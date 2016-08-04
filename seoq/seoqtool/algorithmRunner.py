from .algorithm import Algorithm


class AlgorithmRunner(object):

    def run(self):
        one = Algorithm('inqbation.com')
        print 'done 1'
        two = Algorithm('penncoursereview.com')
        print 'done 2'
        three = Algorithm('doyouget-it.com')
        print 'done 3'
        four = Algorithm('phantompilots.com')
        print 'done 4'
        five = Algorithm('gojagsports.com')
        print 'done 5'
        six = Algorithm('allafrica.com/soccer/')
        print 'done 6'

        print one.getSiteScore()[0]
        print two.getSiteScore()[0]
        print three.getSiteScore()[0]
        print four.getSiteScore()[0]
        print five.getSiteScore()[0]
        print six.getSiteScore()[0]
