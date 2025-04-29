from input.input_process import ReadFile
from utils.input_helper import StructureNormalizer, TextCleaner, FieldExtractor, ReferenceEnricher
from LLM_process.LLMparse import DocumentPrase, SummaryGenerator
from LLM_process.LLMassignment import ArticleAssignerExtreme

def main(base_path, reference_path, model_name="qwen-plus", batch_size=50):

    reader_base = ReadFile(base_path)
    base_content = reader_base.get_file_content()

    reader_reference = ReadFile(reference_path)
    reference_content = reader_reference.get_file_content()

    structure_process = StructureNormalizer()
    text_process = TextCleaner()

    base_content = structure_process.move_paragraph_to_title(base_content)
    base_content = text_process.process(base_content)

    reference_content = structure_process.move_paragraph_to_title(reference_content)
    reference_content = text_process.process(reference_content)

    doc_process = DocumentPrase()
    summary_process = SummaryGenerator(model_name=model_name)

    base_phrase = doc_process(base_content)
    reference_phrase = summary_process.generate_document_summary(reference_content)
    summary_output = summary_process.generate_document_summary(reference_phrase)

    base_file_extractor = FieldExtractor(['title', 'length'])
    reference_file_extractor = FieldExtractor(['id', 'summary', 'length'])

    base_articles = base_file_extractor(base_phrase)
    reference_articles = reference_file_extractor(summary_output['section_summaries'])

    assigner = ArticleAssignerExtreme(model_name=model_name, batch_size=batch_size)
    new_articles = assigner.assign(base_articles, reference_articles)

    new_file_productor = ReferenceEnricher(summary_output)
    new_file_production = new_file_productor(new_articles)

    return new_file_production

if __name__ == '__main__':
    base_path = '/home/baishi/PycharmProjects/text_gen/test/base.docx'
    reference_path = '/home/baishi/PycharmProjects/text_gen/test/reference.docx'
    result = main(base_path, reference_path, model_name="qwen-plus", batch_size=50)
    print(result)

