from utils import*

def save_supplement_for_model(dict_omics:dict, path_save_model:str):
    for xom in list(dict_omics.keys()):
        tmpfile = pd.read_csv(dict_omics[xom], index_col=0)
        tmpcolname = list(tmpfile.columns)
        tmpcoldf = pd.DataFrame(tmpcolname)
        path_w = path_save_model + "_" + xom + ".csv"
        tmpcoldf.to_csv(path_w, header=False, index=False)

def save_supplement_label_template(path_label:str, path_save_model:str):
    dflabel = pd.read_csv(path_label, index_col=0)
    dflabel[:] = ""
    path_w = path_save_model + "_" + "template_label.csv"
    dflabel.to_csv(path_w)


def build_model(perc_tst:float, path_save_model:str, path_labels:str, dict_omics:dict, regr_or_clas:int, class_num:int=0):
    dict_omics = dict(sorted(dict_omics.items()))
    ## Read the default config FIRST
    config = read_config("model.cfg")
    if regr_or_clas == 1:
        config["Transformer_output"] = class_num
    else:
        config["Transformer_output"] = 1
    save_config(config, path_save_model)
    batch_size = config["batch_size"]
    epoch_max = config["epoch_max"]
    lr = config["learning_rate"]
    patience = config["patience"]

    dataloader_tr, dataloader_te = dataloader_for_model_train(dict_omics, path_labels, perc_tst, regr_or_clas, batch_size)
    if regr_or_clas == 1:
        train_val_n_omics_clas(dataloader_tr, dataloader_te, dict_omics, path_save_model, epoch_max, patience, lr)
    else:
        train_val_n_omics_regr(dataloader_tr, dataloader_te, dict_omics, path_save_model, epoch_max, patience, lr)
    save_supplement_for_model(dict_omics, path_save_model)
    save_supplement_label_template(path_labels, path_save_model)


def prediction(path_save_result:str, path_model:str, dict_omics:dict):
    dict_omics = dict(sorted(dict_omics.items()))
    ## Read config FIRST
    path_config = path_model + ".cfg"
    config = read_config(path_config)
    ### regr_or_clas:int
    regr_or_clas = 0
    if config["Transformer_output"] > 1:
        regr_or_clas = 1
    ## RUN prediction
    y = dataloader_and_model_pred(path_model, dict_omics, regr_or_clas, config["batch_size"])
    y = pd.DataFrame(y)
    ## Set colnames: Read label template
    colnamex = pd.read_csv((path_model + "_" + "template_label.csv"), index_col=0)
    y.columns = colnamex.columns.tolist()
    ## Set rownames
    rownamex = pd.read_csv(dict_omics[0], usecols=[0])
    y.index = rownamex.index.tolist()
    ## Write
    y.to_csv(path_save_result)
