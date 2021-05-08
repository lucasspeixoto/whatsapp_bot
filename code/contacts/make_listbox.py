# Criar Infos da listbox

def create_box(base):

    # Formatação Nomes
    file_ok = base.copy()

    listbox_inf, listbox_union = [], []
    for ind in range(0, len(file_ok.columns)):
        listbox_inf.append(file_ok[file_ok.columns[ind]])
    for ind in range(0, len(file_ok)):
        value = str(listbox_inf[0][ind]) + " - " + str(listbox_inf[1][ind])
        listbox_union.append(value)
    return listbox_union
