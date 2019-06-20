from statsmodels.stats.anova import AnovaRM
import pandas as pd

def rm_anova(data=None, subject=None, within=None, between=None, dv=None):
    """
    Returns ANOVA table as dataframe.
    """
    anova = AnovaRM(data=data, 
                    subject=subject, 
                    within=within, 
                    between=between, 
                    depvar=dv)
    fit = anova.fit()
    return fit.anova_table

if __name__ == '__main__':
    df = pd.read_csv('rm_anova.csv')
    
    results = rm_anova(data=df, 
                       subject='subject', 
                       within=['within1', 'within2'], 
                       dv='dv')
