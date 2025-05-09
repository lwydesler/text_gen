from input.input_process import ReadFile
from utils.input_helper import StructureNormalizer, TextCleaner, FieldExtractor, ReferenceEnricher
from LLM_process.LLMparse import DocumentPrase, SummaryGenerator
from LLM_process.LLMassignment import ArticleAssignerExtreme
from LLM_process.LLMgenerator import ParagraphGenerator

def main(base_path, reference_path, apikey, model_name="qwen-plus", batch_size=50):

    reader_base = ReadFile(base_path)
    print('-'*20+'reader_base:base_content'+'-'*20)
    base_content = reader_base.get_file_content()
    #print(base_content)

    reader_reference = ReadFile(reference_path)
    print('-'*20+'reader_reference:reference_content'+'-'*20)
    reference_content = reader_reference.get_file_content()
    #print(reference_content)

    structure_process = StructureNormalizer()
    text_process = TextCleaner()


    print('-'*20+'structure_process:base_content'+'-'*20)
    base_content = structure_process.move_paragraph_to_title(base_content)
    base_content = text_process.process(base_content)

    print('-'*20+'structure_process:reference_content'+'-'*20)
    reference_content = structure_process.move_paragraph_to_title(reference_content)
    reference_content = text_process.process(reference_content)

    doc_process = DocumentPrase()
    summary_process = SummaryGenerator(model_name=model_name, api_key=apikey)

    print('-'*20+'doc_process:base_phrase'+'-'*20)
    base_phrase = doc_process.extract_paragraphs(base_content)

    print('-'*20+'doc_process:reference_phrase'+'-'*20)
    reference_phrase =  doc_process.extract_paragraphs(reference_content)

    print('-'*20+'summary_process:summary_output'+'-'*20)
    summary_output = summary_process.generate_document_summary(reference_phrase)

    base_file_extractor = FieldExtractor(['title', 'length'])
    reference_file_extractor = FieldExtractor(['id', 'summary', 'length'])

    print('-'*20+'base_file_extractor:base_articles'+'-'*20)
    base_articles = base_file_extractor.extract(base_phrase)

    print('-'*20+'reference_file_extractor:reference_articles'+'-'*20)
    reference_articles = reference_file_extractor.extract(summary_output['section_summaries'])

    print('-'*20+'assigner:new_articles'+'-'*20)
    assigner = ArticleAssignerExtreme(model_name=model_name, batch_size=batch_size, current_api_key=apikey)
    new_articles = assigner.assign(base_articles, reference_articles)

    print('-'*20+'new_file_productor:new_file_production'+'-'*20)
    new_file_productor = ReferenceEnricher(summary_output)
    new_file_production = new_file_productor.enrich(new_articles)

    print('-'*20+'ParagraphGenerator:ParagraphGenerator'+'-'*20)
    # generator = ParagraphGenerator(model_name=model_name)
    # generated_results = generator.generate_all_chapters(new_file_production)
    return new_file_production

if __name__ == '__main__':
    base_path = '/home/baishi/PycharmProjects/text_gen/test/base.docx'
    reference_path = '/home/baishi/PycharmProjects/text_gen/test/reference.docx'
    api_key = ''
    result = main(base_path, reference_path, apikey=api_key, model_name="qwen-plus", batch_size=50)
    print(result)

