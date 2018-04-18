import ParameterClasses as P
import MarkovModel as MarkovCls
import SupportMarkovModel as SupportMarkov
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs

# create and simulate cohort
cohort = MarkovCls.Cohort(
    id=1,
    therapy=P.Therapies.ANTICOAG)

simOutputs = cohort.simulate()

# print outcomes (means and CIs)
SupportMarkov.print_outcomes(simOutputs, 'Treatment:')
