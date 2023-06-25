
python ./zad1.py -trn ../data/iris_trn.txt -tst ../data/iris_tst.txt -o "zad1_iris.txt"
python ./zad1.py -trn ../data/epj_trn.txt -tst ../data/epj_tst.txt -o "zad1_epj.txt"

python ./zad1.py -trn ../data/iris_trn.txt -tst ../data/iris_tst.txt -o "zad1_iris.txt"

python ./zad2.py -trn ../data/iris_trn.txt -tst ../data/iris_tst.txt -o "zad2_iris.txt"
python ./zad2.py -trn ../data/epj_trn.txt  -tst  ../data/epj_tst.txt -o "zad2_epj.txt"

python ./zad3.py --train_file ../data/epj_trn.txt --classes 2 3 --max_iter_count 1000 --output_file "zad3_epj_2_3.txt"

python ./zad6.py -trn ../data/iris_trn.txt -tst ../data/iris_tst.txt -o "zad6_iris.txt"
python ./zad6.py -trn ../data/epj_trn.txt -tst ../data/epj_tst.txt -o "zad6_epj.txt"