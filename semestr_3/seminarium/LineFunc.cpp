
    class LineFunction {
        double a, b; //dane

        // operacja
        double operator()(double x) const{ 
            return a * x + b;
        }
    };
