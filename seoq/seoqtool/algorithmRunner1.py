from .algorithm import Algorithm


class AlgorithmRunner1(object):

    key = ['hotels', 'dc']

    def run(self):
        one = Algorithm('hotels.com/de1467359/hotels-washington-district-of-columbia/')
        print 'done 1'
        two = Algorithm('tripadvisor.com/Hotels-g28970-Washington_DC_District_of_Columbia-Hotels.html')
        print 'done 2'
        three = Algorithm('expedia.com/Washington-Hotels.d178318.Travel-Guide-Hotels')
        print 'done 3'
        four = Algorithm('hipmunk.com/Hotels-in-Washington-DC')
        print 'done 4'
        five = Algorithm('marriott.com/hotel-search/washington-dc.hotels.united-states/')
        print 'done 5'

        one.getKeywordClass('hotels.com/de1467359/hotels-washington-district-of-columbia/', self.key)
        print 'done 1'
        two.getKeywordClass('tripadvisor.com/Hotels-g28970-Washington_DC_District_of_Columbia-Hotels.html', self.key)
        print 'done 2'
        three.getKeywordClass('expedia.com/Washington-Hotels.d178318.Travel-Guide-Hotels', self.key)
        print 'done 3'
        four.getKeywordClass('hipmunk.com/Hotels-in-Washington-DC', self.key)
        print 'done 4'
        five.getKeywordClass('marriott.com/hotel-search/washington-dc.hotels.united-states/', self.key)
        print 'done 5'

        algs = [one, two, three, four, five]
        for backlinkvar in range(4):
            for trustflowvar in range(3):
                for robotsvar in range(3):
                    for listingvar in range(3):
                        for keyVar in range(4):
                            print 'change'
                            for alg in algs:
                                alg.changeVar(
                                    backlinkvar * 2 + 1,
                                    trustflowvar + 1, robotsvar * 3 + 1,
                                    listingvar * 3 + 1, keyVar * 3 + 1)
                            if self.runSites(algs):
                                print str(backlinkvar) + '' + str(trustflowvar) + '' + str(robotsvar) + '' + str(listingvar) + '' + str(keyVar)
        return "done"

    def runSites(self, algs):
        scores = [100.00, 100.00, 100.00, 100.00, 100.00]
        for count in range(5):
            alg = algs[count]
            scores[count] = alg.getKeywordScore(self.key)
            if count > 0 and count < 4:
                if scores[count] > scores[count - 1]:
                    return False
        return True
