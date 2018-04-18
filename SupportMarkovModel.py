import InputData as Settings
import scr.FormatFunctions as F
import scr.StatisticalClasses as Stat
import scr.EconEvalClasses as Econ


def print_outcomes(simOutput, treatment_name):
    """ prints the outcomes of a simulated cohort
    :param simOutput: output of a simulated cohort
    :param treatment_name: the name of the selected treatment
    """
    # mean and confidence interval text of patient survival time
    survival_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_survival_times().get_mean(),
        interval=simOutput.get_sumStat_survival_times().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # mean and confidence interval text of time to stroke
    strokes_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_count_strokes().get_mean(),
        interval=simOutput.get_sumStat_count_strokes().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

  # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_cost().get_mean(),
        interval=simOutput.get_sumStat_discounted_cost().get_t_CI(alpha=Settings.ALPHA),
        deci=0,
        form=F.FormatNumber.CURRENCY)

    # mean and confidence interval text of discounted total utility
    utility_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_utility().get_mean(),
        interval=simOutput.get_sumStat_discounted_utility().get_t_CI(alpha=Settings.ALPHA),
        deci=2)



    # print outcomes
    print(treatment_name)
    print("  Estimate of mean and {:.{prec}%} confidence interval of survival time:".format(1 - Settings.ALPHA, prec=0),
          survival_mean_CI_text)
    print("  Estimate of mean and {:.{prec}%} confidence interval of number of strokes:".format(1 - Settings.ALPHA, prec=0),
          strokes_mean_CI_text)
    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")



def print_comparative_outcomes(simOutputs_none, simOutputs_anticoag):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under anticoagulation treatment compared to none treatment
    :param simOutputs_none: output of a cohort simulated under none treatment
    :param simOutputs_anticoag: output of a cohort simulated under anticoagulation treatment
    """

    # increase in survival time under anticoagulation treatment with respect to none treatment
    increase_survival_time = Stat.DifferenceStatIndp(
        name='Increase in survival time',
        x=simOutputs_anticoag.get_survival_times(),
        y_ref=simOutputs_none.get_survival_times())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_survival_time.get_mean(),
        interval=increase_survival_time.get_t_CI(alpha=Settings.ALPHA),
        deci=2)
    print("Average increase in survival time "
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)

    # change in number of strokes under anticoagulation treatment with respect to none treatment
    change_number_strokes = Stat.DifferenceStatIndp(
        name='Change in number of strokes',
        x=simOutputs_anticoag.get_if_developed_stroke(),
        y_ref=simOutputs_none.get_if_developed_stroke())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=change_number_strokes.get_mean(),
        interval=change_number_strokes.get_t_CI(alpha=Settings.ALPHA),
        deci=2)
    print("Average change in number of strokes "
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)

    # increase in discounted total cost under anticoagulation treatment with respect to none treatment
    increase_discounted_cost = Stat.DifferenceStatIndp(
        name='Increase in discounted cost',
        x=simOutputs_anticoag.get_costs(),
        y_ref=simOutputs_none.get_costs())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_discounted_cost.get_mean(),
        interval=increase_discounted_cost.get_t_CI(alpha=Settings.ALPHA),
        deci=0,
        form=F.FormatNumber.CURRENCY)
    print("Average increase in discounted cost "
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)

    # increase in discounted total utility under anticoagulation treatment with respect to none treatment
    increase_discounted_utility = Stat.DifferenceStatIndp(
        name='Increase in discounted cost',
        x=simOutputs_anticoag.get_utilities(),
        y_ref=simOutputs_none.get_utilities())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_discounted_utility.get_mean(),
        interval=increase_discounted_utility.get_t_CI(alpha=Settings.ALPHA),
        deci=2)
    print("Average increase in discounted utility "
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)


def report_CEA(simOutputs_none, simOutputs_anticoag):
    """ performs cost-effectiveness and cost-benefit analyses
    :param simOutputs_none: output of a cohort simulated under none treatment
    :param simOutputs_anticoag: output of a cohort simulated under anticoagulation treatment
    """

    # define two strategies
    none_treatment_strategy = Econ.Strategy(
        name='No Treatment',
        cost_obs=simOutputs_none.get_costs(),
        effect_obs=simOutputs_none.get_utilities()
    )
    anticoag_treatment_strategy = Econ.Strategy(
        name='Anticoagulant Treatment',
        cost_obs=simOutputs_anticoag.get_costs(),
        effect_obs=simOutputs_anticoag.get_utilities()
    )

    # do CEA
    CEA = Econ.CEA(
        strategies=[none_treatment_strategy, anticoag_treatment_strategy],
        if_paired=False
    )

    # show the CE plane
    CEA.show_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional discounted utility',
        y_label='Additional discounted cost',
        show_names=True,
        show_clouds=True,
        show_legend=True,
        figure_size=6,
        transparency=0.3
    )
    # report the CE table
    CEA.build_CE_table(
        interval=Econ.Interval.CONFIDENCE,
        alpha=Settings.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
    )


def report_CBA(simOutputs_none, simOutputs_anticoag):
    """ performs cost-effectiveness and cost-benefit analyses
    :param simOutputs_none: output of a cohort simulated under none treatment
    :param simOutputs_anticoag: output of a cohort simulated under anticoagulation treatment
    """
    # increase in discounted total cost under anticoagulation treatment with respect to none treatment
    increase_discounted_cost = Stat.DifferenceStatIndp(
        name='Increase in discounted cost',
        x=simOutputs_anticoag.get_costs(),
        y_ref=simOutputs_none.get_costs())
    # increase in discounted total utility under anticoagulation treatment with respect to none treatment
    increase_discounted_utility = Stat.DifferenceStatIndp(
        name='Increase in discounted cost',
        x=simOutputs_anticoag.get_utilities(),
        y_ref=simOutputs_none.get_utilities())
    print ("I recommend the folllwing willingness-to-pay level for adopting this anticoagulation drug: >",'${:,.2f}'.format(increase_discounted_cost.get_mean()/increase_discounted_utility.get_mean()))


    # define two strategies
    none_treatment_strategy = Econ.Strategy(
        name='No Treatment',
        cost_obs=simOutputs_none.get_costs(),
        effect_obs=simOutputs_none.get_utilities()
    )
    anticoag_treatment_strategy = Econ.Strategy(
        name='Anticoagulant Treatment',
        cost_obs=simOutputs_anticoag.get_costs(),
        effect_obs=simOutputs_anticoag.get_utilities()
    )

    # CBA
    NBA = Econ.CBA(
        strategies=[none_treatment_strategy, anticoag_treatment_strategy],
        if_paired=False
    )

    # show the net monetary benefit figure
    NBA.graph_deltaNMB_lines(
        min_wtp=0,
        max_wtp=50000,
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay for one additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval=Econ.Interval.CONFIDENCE,
        show_legend=True,
        figure_size=6
    )

