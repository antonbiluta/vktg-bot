from docxtpl import DocxTemplate
from pdf2image import convert_from_path
from docx2pdf import convert


def generate8mart(name_to, text, name_from, filepath):
    file = filepath+'.docx'
    doc = DocxTemplate(file)
    context = {'name_to': name_to,
               'text': text,
               'name_from': name_from
               }
    doc.render(context)
    temp = filepath + '-final.docx'
    doc.save(temp)
    return temp


def generateRasp(group, subgroup, faculty, week, pn, vt, sr, ct, pt, sb, filepath):
    file = filepath+'.docx'
    doc = DocxTemplate(file)

    context = {'group':group,
               'subgroup':subgroup,
               'faculty':faculty,
               'неделя':week,
               'director':'Billuchi'
               }


    num = [1,2,3,4,5]
    for x in num:
        predmet = f'predmet_pn{x}'
        context.update({predmet: '-'})
        predmet = f'predmet_vt{x}'
        context.update({f'{predmet}': '-'})
        predmet = f'predmet_sr{x}'
        context.update({f'{predmet}': '-'})
        predmet = f'predmet_ct{x}'
        context.update({f'{predmet}': '-'})
        predmet = f'predmet_pt{x}'
        context.update({f'{predmet}': '-'})
        predmet = f'predmet_sb{x}'
        context.update({f'{predmet}': '-'})

    for block in pn:
        predmet = f'predmet_pn{block[0]}'
        context.update({f'{str(predmet)}': f'{str(block[2])}'})
    for block in vt:
        predmet = f'predmet_vt{block[0]}'
        context.update({f'{predmet}': f'{block[2]}'})
    for block in sr:
        predmet = f'predmet_sr{block[0]}'
        context.update({f'{predmet}': f'{block[2]}'})
    for block in ct:
        predmet = f'predmet_ct{block[0]}'
        context.update({f'{predmet}': f'{block[2]}'})
    for block in pt:
        predmet = f'predmet_pt{block[0]}'
        context.update({f'{predmet}': f'{block[2]}'})
    for block in sb:
        predmet = f'predmet_sb{block[0]}'
        context.update({f'{predmet}': f'{block[2]}'})

    doc.render(context)
    temp = filepath+'-final.docx'
    doc.save(temp)


def docxPdf(path):
    convert(path)
    return True

def pdfImage(path):
    return convert_from_path(path, 500, poppler_path='C:/Program Files/poppler-0.68.0/bin')
