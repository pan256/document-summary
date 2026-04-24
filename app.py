"""
文档摘要 Agent - 命令行版本
无需前端，直接生成摘要
"""
import sys
import os
import io

# 设置标准输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from document_loader import DocumentLoader
from summary_generator import SummaryGenerator
from docx import Document as WordDocument


def save_as_txt(content, output_path):
    """保存为 TXT 文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def save_as_word(content, output_path):
    """保存为 Word 文件"""
    doc = WordDocument()
    for line in content.split('\n'):
        doc.add_paragraph(line)
    doc.save(output_path)


def save_as_pdf(content, output_path):
    """保存为 PDF 文件（自适应页面）"""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.units import cm

    # 注册中文字体
    font_path = "C:/Windows/Fonts/msyh.ttc"
    try:
        pdfmetrics.registerFont(TTFont('SimHei', font_path))
    except:
        pass

    # 创建文档
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    # 创建样式
    styles = getSampleStyleSheet()
    style = ParagraphStyle(
        'Chinese',
        fontName='SimHei',
        fontSize=12,
        leading=18,
        wordWrap='CJK'
    )
    title_style = ParagraphStyle(
        'Title',
        fontName='SimHei',
        fontSize=14,
        leading=20,
        spaceAfter=10,
        wordWrap='CJK'
    )

    # 构建内容
    story = []
    lines = content.split('\n')
    for line in lines:
        if line.startswith('==='):
            story.append(Spacer(1, 0.3*cm))
        elif line in ['摘要结果:', '关键要点:']:
            story.append(Paragraph(line, title_style))
            story.append(Spacer(1, 0.2*cm))
        elif line.strip():
            story.append(Paragraph(line, style))

    # 生成PDF
    doc.build(story)


def main():
    """主函数"""
    # 检查参数
    if len(sys.argv) < 2:
        print("使用方法: python app.py <文档路径>")
        print("支持格式: PDF、Word、TXT")
        print("示例: python app.py document.pdf")
        return

    file_path = sys.argv[1]

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在 - {file_path}")
        return

    # 检查文件格式
    ext = os.path.splitext(file_path)[1].lower()
    supported = ['.pdf', '.docx', '.doc', '.txt']
    if ext not in supported:
        print(f"错误: 不支持的格式 - {ext}")
        print(f"支持格式: {supported}")
        return

    print(f"正在处理: {file_path}")
    print("-" * 50)

    try:
        # 加载文档
        loader = DocumentLoader()
        text = loader.load(file_path)
        print(f"文档长度: {len(text)} 字符")

        # 生成摘要
        print("\n正在生成摘要...")
        generator = SummaryGenerator()
        summary = generator.generate_summary(text)

        print("\n" + "=" * 50)
        print("摘要结果:")
        print("=" * 50)
        print(summary)

        # 提取关键要点
        print("\n" + "=" * 50)
        print("关键要点:")
        print("=" * 50)
        key_points = generator.extract_key_points(text)
        print(key_points)

        # 保存摘要到文件（保持原格式）
        ext = os.path.splitext(file_path)[1].lower()
        output_path = os.path.splitext(file_path)[0] + "_摘要" + ext

        full_content = "=" * 50 + "\n摘要结果:\n" + "=" * 50 + "\n" + summary + "\n\n" + "=" * 50 + "\n关键要点:\n" + "=" * 50 + "\n" + key_points + "\n"

        if ext == '.pdf':
            save_as_pdf(full_content, output_path)
        elif ext in ['.docx', '.doc']:
            save_as_word(full_content, output_path)
        else:
            save_as_txt(full_content, output_path)

        print(f"\n摘要已保存到: {output_path}")

    except Exception as e:
        print(f"处理失败: {e}")


if __name__ == "__main__":
    main()