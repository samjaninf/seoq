from .algorithm import Algorithm


class AlgorithmRunner1(object):

    key = ['hotels', 'in', 'dc']

    def run(self):
        one = Algorithm('https://www.hotels.com/de1467359/hotels-washington-district-of-columbia/')
        print 'done 1'
        two = Algorithm('https://www.tripadvisor.com/Hotels-g28970-Washington_DC_District_of_Columbia-Hotels.html')
        print 'done 2'
        three = Algorithm('https://www.expedia.com/Washington-Hotels.d178318.Travel-Guide-Hotels')
        print 'done 3'
        four = Algorithm('https://www.hipmunk.com/Hotels-in-Washington-DC')
        print 'done 4'
        five = Algorithm('http://www.marriott.com/hotel-search/washington-dc.hotels.united-states/')
        print 'done 5'

        one.getKeywordClass('https://www.hotels.com/de1467359/hotels-washington-district-of-columbia/')
        print 'done 1'
        two.getKeywordClass('https://www.tripadvisor.com/Hotels-g28970-Washington_DC_District_of_Columbia-Hotels.html', self.key)
        print 'done 2'
        three.getKeywordClass('https://www.expedia.com/Washington-Hotels.d178318.Travel-Guide-Hotels', self.key)
        print 'done 3'
        four.getKeywordClass('https://www.hipmunk.com/Hotels-in-Washington-DC', self.key)
        print 'done 4'
        five.getKeywordClass('http://www.marriott.com/hotel-search/washington-dc.hotels.united-states/', self.key)
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
            scores[count] = alg.getKeywordScore(self.key)
            if count > 0:
                if scores[count] > scores[count - 1]:
                    return False
        return True
