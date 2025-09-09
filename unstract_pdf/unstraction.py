import os
import time
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader
#from tqdm import tqdm

# Cấu hình
PDF_FOLDER = "data"  # Thư mục chứa PDF đầu vào
TXT_FOLDER = "data_unstracted"   # Thư mục lưu TXT đầu ra
LANGUAGES = "vie+eng"      # Ngôn ngữ OCR (tiếng Việt + Anh)

def process_slide_pdfs():
    """Xử lý tất cả file PDF trong thư mục và lưu dưới dạng TXT"""
    # Tạo thư mục đầu ra nếu chưa tồn tại
    Path(TXT_FOLDER).mkdir(parents=True, exist_ok=True)
    
    # Khởi tạo DirectoryLoader với cấu hình OCR
    loader = DirectoryLoader(
        PDF_FOLDER,
        glob="*.pdf",
        loader_cls=UnstructuredPDFLoader,
        loader_kwargs={
            "mode": "elements",         # Tách thành các phần tử riêng biệt
            "strategy": "hi_res",       # Sử dụng OCR cho hình ảnh
            "ocr_languages": LANGUAGES, # Hỗ trợ tiếng Việt và Anh
            "chunking_strategy": "by_title",  # Nhóm theo tiêu đề slide
            "infer_table_structure": True,    # Nhận diện bảng biểu
            "extract_page_breaks": True,      # Giữ ngắt trang
            "pdf_extract_line_breaks": True   # Giữ ngắt dòng
        },
        show_progress=True,  # Hiển thị thanh tiến trình
        use_multithreading=True  # Sử dụng đa luồng để tăng tốc
    )
    
    print("### Đang trích xuất văn bản từ các slide PDF...")
    start_time = time.time()
    
    try:
        # Load và xử lý tất cả tài liệu
        docs = loader.load()
        
        # Nhóm kết quả theo tên file nguồn
        grouped_docs = {}
        for doc in docs:
            source = doc.metadata["source"]
            if source not in grouped_docs:
                grouped_docs[source] = []
            grouped_docs[source].append(doc.page_content)
        
        # Lưu kết quả cho từng file
        for source, contents in grouped_docs.items():
            # Tạo tên file đầu ra
            filename = Path(source).stem + ".txt"
            txt_path = Path(TXT_FOLDER) / filename
            
            # Kết hợp nội dung và lưu file
            full_text = "\n\n".join(contents)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)
        
        process_time = time.time() - start_time
        print(f">>> Đã xử lý thành công {len(grouped_docs)} file PDF")
        print(f">>> Tổng thời gian: {process_time:.2f} giây")
        print(f">>> Kết quả được lưu tại: {Path(TXT_FOLDER).resolve()}")
        
        return True
        
    except Exception as e:
        print(f"X >> Lỗi trong quá trình xử lý: {str(e)}")
        return False

if __name__ == "__main__":
    # Kiểm tra file PDF
    pdf_files = list(Path(PDF_FOLDER).glob("*.pdf"))
    if not pdf_files:
        print(f"X >> Không tìm thấy file PDF nào trong thư mục '{PDF_FOLDER}'")
    else:
        print(f">>> Tìm thấy {len(pdf_files)} file PDF để xử lý")
        success = process_slide_pdfs()
        
        if success:
            print("\n+> Hoàn thành tất cả quá trình trích xuất!")
            print("->> Bạn có thể tìm thấy các file TXT trong thư mục 'data'")