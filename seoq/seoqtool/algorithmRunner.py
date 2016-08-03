from .algorithm import Algorithm


class AlgorithmRunner(object):

    def run(self):
        one = Algorithm('en.wikipedia.org/wiki/Agile_software_development')
        print 'done 1'
        two = Algorithm('howdesign.com/editors-picks/dont-go-chasing-waterfalls-agile-web-design/')
        print 'done 2'
        three = Algorithm('sixrevisions.com/web-development/agile/')
        print 'done 3'
        four = Algorithm('amazon.com/Agile-Development-Rails-Pragmatic-Programmers/dp/1934356549')
        print 'done 4'
        five = Algorithm('agileana.com/')
        print 'done 5'

        one.getKeywordClass('en.wikipedia.org/wiki/Agile_software_development', ['agile', 'web', 'development'])
        print 'done 1'
        two.getKeywordClass('howdesign.com/editors-picks/dont-go-chasing-waterfalls-agile-web-design/', ['agile', 'web', 'development'])
        print 'done 2'
        three.getKeywordClass('sixrevisions.com/web-development/agile/', ['agile', 'web', 'development'])
        print 'done 3'
        four.getKeywordClass('amazon.com/Agile-Development-Rails-Pragmatic-Programmers/dp/1934356549', ['agile', 'web', 'development'])
        print 'done 4'
        five.getKeywordClass('agileana.com/', ['agile', 'web', 'development'])
        print 'done 5'

        algs = [one, two, three, four, five]
        for count in range(5):
            alg = algs[count]
            print alg.getKeywordScore(['agile', 'web', 'development'])
