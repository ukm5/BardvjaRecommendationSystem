def pypdf2_parser(path_to_pdf):
    import PyPDF2
    pdf_contents = {}
    pdf_reader = PyPDF2.PdfFileReader(path_to_pdf)
    pdf_contents['total_pages'] = pdf_reader.numPages
    pdf_info = pdf_reader.getDocumentInfo()
    pdf_contents['author'] = pdf_info.author
    pdf_contents['title'] = str(pdf_info.title).lower()
    pdf_contents['creator'] = pdf_info.creator
    try:
        pdf_contents['subject'] = pdf_info['/Subject'].split(' ')[0:-1]
    except:
        pdf_contents['subject'] = 'Unknown'
    try:
        pdf_contents['complete_pdf'] = pdf_contents['title'] + ' '.join([pdf_reader.getPage(i).extractText() for i in range(pdf_contents['total_pages'])])
    except:
        print(f"Error: While trying to combine title and text there is issue at this file: {path_to_pdf}")
    return pdf_contents

def make_training_dataframe(path_to_training_papers):
    import os
    import pandas as pd

#     os.chdir(path_to_training_papers)
    print("Hello World!")
    train_data = {}
    print(os.listdir(path_to_training_papers))
#     for idx, filename in enumerate(os.listdir()):
#         if filename != '.DS_Store':
#             path_to_pdf = path_to_training_papers+filename
#             print(f"Parsing this paper now: {path_to_pdf}")
#             train_data[idx] = pypdf2_parser(path_to_pdf)

    return pd.DataFrame(train_data.values())
