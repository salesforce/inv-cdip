# The INV-CDIP Dataset

## Introduction
This is the INV-CDIP dataset used in our paper "Field Extraction from Forms with Unlabeled Data". The dataset contains 
an unlabeled set and a labeled set. The unlabeled set contains around 200k invoices. The labeled set contains 350 invoices 
with 7 field annotated including invoice number, purchase order, invoice date, due date, amount due, total amount and 
total tax.

## Download Dataset
* Document ids are stored in train_set.txt and test_set.txt.
* You may browse a document using https://www.industrydocuments.ucsf.edu/docs/$document_id.
* Use the following script to download data automatically.
```buildoutcfg
#install packages
bash install.sh
#download labeled data
python download_data.py --download --split labeled
#download unlabeled data
python download_data.py --download --split unlabeled
```

## Annotation Description
* Annotations are in ./annotation folder.

  * In each json file, field label is annotated in ['Fields']['value']['label'].

  * Field value is annotated in ['Fields']['value']['tag'].

  * Field value location is annotated in ['Fields']['value']['bbox'].
  
  * The key of a field value is annotated in ['Fields']['key']['tag'].
  
  * Key location is annotated in ['Fields']['key']['bbox'].


* Use the following script to visualize the annotations.
```buildoutcfg
#visualize annotations
python download_data.py --vis
```

## Citation
Please cite our paper if you use this dataset.
```buildoutcfg
@article{gao2021field,
  title={Field Extraction from Forms with Unlabeled Data},
  author={Gao, Mingfei and Chen, Zeyuan and Naik, Nikhil and Hashimoto, Kazuma and Xiong, Caiming and Xu, Ran},
  journal={ACL Spa-NLP Workshop},
  year={2022}
}
```

## License
The INV-CDIP dataset is released under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). 
The underlying documents to which the dataset refers are from the [Tobacco Collections of Industry Documents Library](https://www.industrydocuments.ucsf.edu/). 
Please see [Copyright and Fair Use](https://www.industrydocuments.ucsf.edu/help/copyright/) for more information.

## Contact
Please contact mingfei.gao@salesforce.com if you have questions.
