
python ./zad1.py -trn ../data/iris_trn.txt -tst ../data/iris_tst.txt -o "zad1_iris.txt"
python ./zad1.py -trn ../data/epj_trn.txt -tst ../data/epj_tst.txt -o "zad1_epj.txt"

python ./zad1.py -trn ../data/iris_trn.txt -tst ../data/iris_tst.txt -o "zad1_iris.txt"

python ./zad2.py -trn ../data/iris_trn.txt -tst ../data/iris_tst.txt -o "zad2_iris.txt"
python ./zad2.py -trn ../data/epj_trn.txt  -tst  ../data/epj_tst.txt -o "zad2_epj.txt"

python ./zad3.py -trn ../data/epj_trn.txt --classes 2 3 --max_iter_count 1000 --output_file "zad3_epj_2_3.txt"
python ./zad3.py -trn ../data/iris_trn.txt --classes 1 2 --max_iter_count 1000 --output_file "zad3_irys_1_2.txt"

python ./zad4.py -trn ../data/epj_trn.txt --classes 2 3  --output_file "zad4_epj_2_3.txt"
python ./zad4.py -trn ../data/iris_trn.txt --classes 1 2  --output_file "zad4_irys_1_2.txt"
python ./zad4.py -trn ../data/iris_trn.txt --classes 2 3  --output_file "zad4_irys_2_3.txt"

python ./zad6.py -trn ../data/iris_trn.txt -tst ../data/iris_tst.txt -o "zad6_iris.txt"
python ./zad6.py -trn ../data/epj_trn.txt -tst ../data/epj_tst.txt -o "zad6_epj.txt"