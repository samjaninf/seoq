from .algorithm import Algorithm


class AlgorithmRunner(object):

    def run(self):
        one = Algorithm('agileana.com')
        print 'done 1'
        two = Algorithm('cnn.com')
        print 'done 2'
        three = Algorithm('espn.com')
        print 'done 3'
        four = Algorithm('apple.com')
        print 'done 4'
        five = Algorithm('ae.com')
        print 'done 5'
        six = Algorithm('google.com')
        print 'done 6'

        print one.getSiteScore()[0]
        print two.getSiteScore()[0]
        print three.getSiteScore()[0]
        print four.getSiteScore()[0]
        print five.getSiteScore()[0]
        print six.getSiteScore()[0]
