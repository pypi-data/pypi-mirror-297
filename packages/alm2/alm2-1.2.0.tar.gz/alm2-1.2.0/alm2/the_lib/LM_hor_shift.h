double logL_diretta(long m, int hor_shift);

double LM_logL(double x, double y, long m, int hor_shift);

long* opterrNoPrint_logL(long *maxprec, double* toterr, double n);


double loggamma_LM( double probabilities[],  double psi_0);

long init_params(int PREC, double counts[], int categories );

double logL_diretta_global();
