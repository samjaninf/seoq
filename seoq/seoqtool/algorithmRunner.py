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
        for backlinkvar in range(3):
            for trustflowvar in range(3):
                for robotsvar in range(3):
                    for listingvar in range(3):
                        for keyVar in range(3):
                            print 'change'
                            for alg in algs:
                                alg.changeVar(
                                    backlinkvar * 2 + 1,
                                    trustflowvar + 1, robotsvar * 3 + 1,
                                    listingvar * 3 + 1, keyVar * 3 + 1)
                            if self.runSites(algs):
                                print '__________Solution___________'
                                print (backlinkvar + 1) * 2
                                print (trustflowvar + 1)
                                print (robotsvar + 1) * 3
                                print (listingvar + 1) * 3
                                print (keyVar + 1) * 3
        return "done"

    def runSites(self, algs):
        scores = [100.00, 100.00, 100.00, 100.00, 100.00]
        for count in range(5):
            alg = algs[count]
            scores[count] = alg.getKeywordScore(['agile', 'web', 'development'])
            if count > 0:
                if scores[count] > scores[count - 1]:
                    return False
        return True
