import os
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

import config
from document_processor import DocumentProcessor
from ai_client import GeminiRAGClient
from vector_store import LocalVectorStore

# Paths
INDEX_PATH = "vector_index.json"
TEMP_DOC_PATH = "temp_uploaded_doc.txt"
DEFAULT_KNOWLEDGE_PATH = "knowledge.txt"

# Initialize bot, dispatcher, client and store
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
ai_client = GeminiRAGClient(api_key=config.GEMINI_API_KEY)
vector_store = LocalVectorStore()

# Load existing index if present
if os.path.exists(INDEX_PATH):
    vector_store.load(INDEX_PATH)
    print("Loaded existing vector index.")

# Document processor
doc_processor = DocumentProcessor()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "👋 **Привет! Я твой персональный ИИ RAG-Ассистент.**\n\n"
        "Я умею отвечать на вопросы, основываясь на твоих личных документах!\n\n"
        "📁 **Как мной пользоваться:**\n"
        "1. Отправь мне любой текстовый файл (`.txt` в кодировке UTF-8).\n"
        "2. Я автоматически разобью его на блоки, создам векторный поисковый индекс.\n"
        "3. После этого просто задавай мне любые вопросы по содержанию файла, и я отвечу на них с помощью ИИ Google Gemini!\n\n"
        "💡 *Если файлы еще не загружены, я буду отвечать по встроенной базе знаний о студии Nexus Labs.*"
    )
    
    # Check if we should initialize default knowledge
    if not vector_store.chunks and os.path.exists(DEFAULT_KNOWLEDGE_PATH):
        await index_document(DEFAULT_KNOWLEDGE_PATH)
        welcome_text += "\n\n✅ *Встроенная база знаний о Nexus Labs успешно подключена и проиндексирована!*"
        
    await message.answer(welcome_text, parse_mode="Markdown")

async def index_document(file_path: str):
    """Processes a text file, generates embeddings, and saves the vector store."""
    chunks_data = doc_processor.process_file(file_path)
    if not chunks_data:
        return False

    chunks = [c["content"] for c in chunks_data]
    metadata = [c["metadata"] for c in chunks_data]

    # Generate embeddings
    embeddings = await ai_client.get_embeddings_batch(chunks)
    
    # Add to store
    vector_store.add_documents(chunks, embeddings, metadata)
    vector_store.save(INDEX_PATH)
    return True

@dp.message(F.document)
async def handle_document(message: types.Message):
    document = message.document
    
    # We only accept txt files
    if not document.file_name.endswith('.txt'):
        await message.answer("❌ Пожалуйста, отправьте файл в формате `.txt`.")
        return

    status_msg = await message.answer("📥 Скачиваю и обрабатываю ваш файл...")
    
    try:
        # Download file
        file_info = await bot.get_file(document.file_id)
        await bot.download_file(file_info.file_path, TEMP_DOC_PATH)
        
        # Index document
        await status_msg.edit_text("⚙️ Генерация векторных эмбеддингов ИИ...")
        success = await index_document(TEMP_DOC_PATH)
        
        # Remove temporary file
        if os.path.exists(TEMP_DOC_PATH):
            os.remove(TEMP_DOC_PATH)

        if success:
            await status_msg.edit_text(
                f"✅ **Файл '{document.file_name}' успешно проиндексирован!**\n"
                f"Теперь ты можешь задавать мне вопросы по его содержимому."
            )
        else:
            await status_msg.edit_text("❌ Не удалось прочесть файл. Убедитесь, что кодировка файла — UTF-8.")
            
    except Exception as e:
        await status_msg.edit_text(f"❌ Произошла ошибка при обработке: {e}")

@dp.message()
async def handle_question(message: types.Message):
    query = message.text
    if not query:
        return
        
    # Check if vector store contains documents
    if not vector_store.chunks:
        # Try to load default knowledge if possible
        if os.path.exists(DEFAULT_KNOWLEDGE_PATH):
            await index_document(DEFAULT_KNOWLEDGE_PATH)
        else:
            await message.answer("⚠️ В базе данных пока нет информации. Отправьте текстовый `.txt` файл для индексации!")
            return

    status_msg = await message.answer("🔍 Поиск релевантного контекста и генерация ответа...")
    
    try:
        # 1. Get query embedding
        query_vector = await ai_client.get_embedding(query, is_query=True)
        
        # 2. Search local vector store
        matches = vector_store.search(query_vector, top_k=3)
        
        # Extract matches
        context_chunks = [m["content"] for m in matches]
        
        # 3. Generate answer
        answer = await ai_client.generate_answer(query, context_chunks)
        
        # Highlight matches for clarity (proves it works to clients)
        sources_text = "\n\n*Найденные совпадения (Top-Matches):*\n"
        for i, m in enumerate(matches):
            sources_text += f"- **[{i+1}]** {m['content'][:60]}... (Косинусное сходство: {m['score']:.3f})\n"

        await status_msg.edit_text(f"{answer}{sources_text}", parse_mode="Markdown")
        
    except Exception as e:
        await status_msg.edit_text(f"❌ Произошла ошибка при поиске ответа: {e}")

async def main():
    print("Starting RAG AI Assistant Telegram Bot...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
