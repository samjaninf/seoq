from .algorithm import Algorithm


class AlgorithmRunner(object):

    def run(self):
        one = Algorithm('designologielc.com')
        print 'done 1'
        two = Algorithm('espn.com')
        print 'done 2'

        print one.getSiteScore()[0]
        print two.getSiteScore()[0]
        
