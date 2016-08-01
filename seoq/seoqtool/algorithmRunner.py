from .algorithm import Algorithm


class AlgorithmRunner(object):

    def run(self):
        counter = 0
        for backlinkvar in range(3):
            for trustflowvar in range(3):
                for robotsvar in range(3):
                    for listingvar in range(3):
                        for keyVar in range(3):
                            print counter
                            alg = Algorithm()
                            alg.changeVar(
                                backlinkvar * 2,
                                trustflowvar, robotsvar * 3,
                                listingvar * 3, keyVar * 3)
                            if self.runSites(alg):
                                    return (
                                        backlinkvar,
                                        trustflowvar, robotsvar,
                                        listingvar, keyVar)
                                    print backlinkvar + " " + trustflowvar + " " + robotsvar + " " + listingvar + " " + keyVar
                            counter = counter + 1
        return "no optimal weights"

    def runSites(self, algorithm):
        sites = ['en.wikipedia.org/wiki/Agile_software_development',
                 # 'howdesign.com/editors-picks/dont-go-chasing-waterfalls-agile-web-design/'
                 # 'sixrevisions.com/web-development/agile/',
                 'amazon.com/Agile-Development-Rails-Pragmatic-Programmers/dp/1934356549',
                 'agileana.com/']
        print sites
        scores = [100.00, 100.00, 100.00, 100.00, 100.00]
        for count in range(len(sites)):
            scores[count] = algorithm.getKeywordScore(
                sites[count], ['agile', 'web', 'development'], 1223)
            if count > 0:
                if scores[count] > scores[count - 1]:
                    return False
        return True
