import ParameterClasses as P
import MarkovModel as MarkovCls
import SupportMarkovModel as SupportMarkov
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs

# create and cohort
cohort = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.NONE)

simOutputs = cohort.simulate()

# print outcomes (means and CIs)
SupportMarkov.print_outcomes(simOutputs, 'No treatment:')
