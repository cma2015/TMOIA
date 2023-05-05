import sys, os
from numpy import unique


def resource_path(relative_path:str):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def ifCanBeSaved(xfpath:str):
    ifwrite = False
    if os.path.exists(xfpath):
        os.remove(xfpath)
    with open(xfpath, "x") as fp:
        ifwrite = fp.writable()
    return ifwrite

def check_omics(path_omics:list[str], name_omics:list[str]):
    ## Blank?
    dict_omics:dict[str, str] = {}
    path_omics_list:list[str] = []
    omic_list:list[str] = []
    full_omic = name_omics
    ###
    nom:int = 0
    for xomic in path_omics:
        if full_omic[nom] == '':
            nom = nom + 1
            continue
        if xomic == '':
            nom = nom + 1
            continue
        else:
            path_omics_list.append(xomic)
            omic_list.append(full_omic[nom])
            dict_omics[full_omic[nom]] = xomic
            nom = nom + 1
    ## If omic collision
    if len(unique(path_omics_list)) < len(path_omics_list):#or len(unique(name_omics)) < len(name_omics)
        return False
    else:
        return dict_omics
