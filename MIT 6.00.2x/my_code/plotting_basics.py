import pylab as plt

mySamples = []
myLinear = []
myQuadratic = []
myCubic = []
myExponential = []
exponentBase = 1.5

for i in range(30):
    mySamples.append(i)
    myLinear.append(i)
    myQuadratic.append(i ** 2)
    myCubic.append(i ** 3)
    myExponential.append(exponentBase ** i)


def all_plots_one_graph():
    # all plots on one graph
    plt.plot(mySamples, myLinear)
    plt.plot(mySamples, myQuadratic)
    plt.plot(mySamples, myCubic)
    plt.plot(mySamples, myExponential)


def each_plot_one_graph():
    plt.figure('lin')
    plt.clf()  # clear the figure if we had it opened previously
    plt.title('Linear')
    plt.xlabel('sample points')
    plt.ylabel('linear function')
    plt.plot(mySamples, myLinear, 'b-', linewidth=3.0)

    plt.figure('quad')
    plt.title('Quadratic')
    plt.plot(mySamples, myQuadratic, 'ro')

    plt.figure('cube')
    plt.title('Cubic')
    plt.plot(mySamples, myCubic, 'g^')

    plt.figure('expo')
    plt.title('Exponential')
    plt.plot(mySamples, myExponential, 'r--')

    plt.figure('quad')
    plt.ylabel('quadratic function')


def setting_limits():
    plt.figure('lin')
    plt.clf()
    plt.ylim(0, 1000)
    plt.title('Linear')
    plt.plot(mySamples, myLinear)

    plt.figure('quad')
    plt.clf()
    plt.ylim(0, 1000)
    plt.title('Quadratic')
    plt.plot(mySamples, myQuadratic)


def comparing_results_on_graphs():
    plt.figure('lin quad')
    plt.clf()  # clear the figure if we had it opened previously
    plt.title('linear vs. Quadratic')
    plt.plot(mySamples, myLinear, label='linear')
    plt.plot(mySamples, myQuadratic, label='quadratic')
    plt.legend(loc='upper left')

    plt.figure('cube exp')
    plt.clf()
    plt.title('Cubic vs. Exponential')
    plt.plot(mySamples, myCubic, label='cubic')
    plt.plot(mySamples, myExponential, label='exponential')
    plt.legend()


def subplots():
    plt.figure('lin quad')
    plt.clf()  # clear the figure if we had it opened previously
    plt.subplot(211)  # number of rows, columns, which location to use
    plt.ylim(0, 900)
    plt.plot(mySamples, myLinear, label='linear')
    plt.subplot(212)
    plt.ylim(0, 900)
    plt.plot(mySamples, myQuadratic, label='quadratic')
    plt.title('linear vs. Quadratic')
    plt.legend(loc='upper left')

    plt.figure('cube exp')
    plt.clf()
    plt.subplot(121)
    plt.ylim(0, 140_000)
    plt.plot(mySamples, myCubic, label='cubic')
    plt.subplot(122)
    plt.ylim(0, 140_000)
    plt.plot(mySamples, myExponential, label='exponential')
    plt.title('Cubic vs. Exponential')
    plt.legend()


def changing_scales():
    plt.figure('cube exp log')
    plt.clf()
    plt.plot(mySamples, myCubic, label='cubic')
    plt.plot(mySamples, myExponential, label='exponential')
    plt.yscale('log')
    plt.title('Cubic vs. Exponential')
    plt.legend()

    plt.figure('cube exp linear')
    plt.clf()
    plt.plot(mySamples, myCubic, label='cubic')
    plt.plot(mySamples, myExponential, label='exponential')
    plt.title('Cubic vs. Exponential')
    plt.legend()


class Savings:

    def retire(self, monthly, rate, terms):
        """
        Counts the amount of money saved for retirement.
        monthly - amount of money put to saving each month
        rate - float, the rate at which interest is earned
        terms - how many months to compute over
        """
        base = [0]
        savings = [0]
        monthly_rate = rate/12
        for i in range(terms):
            base += [i]
            savings += [savings[-1]*(1+monthly_rate) + monthly]
        return base, savings

    def display_retire_with_monthlies(self, monthlies, rate, terms):
        """
        Plots a graph displaying the amount of money saved for different amounts of monthly savings.
        :param monthlies: list of different monthly savings
        :param rate: annual interest rate
        :param terms: amount of months to make savings
        :return: None
        """
        plt.figure('retire_diff_month')
        plt.clf()
        for monthly in monthlies:
            xvals, yvals = self.retire(monthly, rate, terms)
            plt.xlabel('Money put to savings')
            plt.ylabel('Total money')
            plt.plot(xvals, yvals, label='retire: '+str(monthly))
            plt.legend()

    def display_retire_with_rates(self, monthly, rates, terms):
        """
        Plots a graph displaying the amount of money saved for different rates.
        :param monthly: monthly savings
        :param rates: list of different annual interest rate
        :param terms: amount of months to make savings
        :return: None
        """
        plt.figure('retire_diff_rate')
        plt.clf()
        for rate in rates:
            xvals, yvals = self.retire(monthly, rate, terms)
            plt.xlabel('Money put to savings')
            plt.ylabel('Total money')
            plt.plot(xvals, yvals, label=f'retire: {monthly} : {int(rate*100)}%')
            plt.legend()

    def display_retire_with_montlies_and_rates(self, monthlies, rates, terms):
        """
        Plots a graph displaying the amount of money saved for different monthly savings and rates.
        :param monthlies: list of different monthly savings
        :param rates: list of different annual interest rate
        :param terms: amount of months to make savings
        :return: None
        """
        plt.figure('retire_diff')
        plt.clf()
        plt.xlim(30*12, 40*12)  # focusing on last 10 years
        month_labels = ['r', 'b', 'g', 'k']
        rate_labels = ['-', 'o', '--']
        for i in range(len(monthlies)):
            monthly = monthlies[i]
            month_label = month_labels[i % len(month_labels)]
            for j in range(len(rates)):
                rate = rates[j]
                rate_label = rate_labels[j % len(rate_labels)]
                xvals, yvals = self.retire(monthly, rate, terms)
                plt.xlabel('Money put to savings')
                plt.ylabel('Total money')
                plt.plot(xvals, yvals, month_label+rate_label, label=f'retire: {monthly} : {int(rate*100)}%')
                plt.legend()


if __name__ == '__main__':
    # all_plots_one_graph()
    # each_plot_one_graph()
    # setting_limits()
    # comparing_results_on_graphs()
    # subplots()
    # changing_scales()

    saving = Savings()
    # saving.display_retire_with_monthlies([600, 800, 1000, 1200], .05, 40*12)
    # saving.display_retire_with_rates(800, [.03, 0.05, 0.07], 40*12)

    saving.display_retire_with_montlies_and_rates([600, 800, 1000, 1200], [.03, 0.05, 0.07], 40*12)
