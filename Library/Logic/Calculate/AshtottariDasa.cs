using System;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json.Linq;

namespace VedAstro.Library
{
    public static class AshtottariDasa
    {
        /// <summary>
        /// Gets the current dasa, bhukti & antaram at inputed time
        /// </summary>
        public static Dasas CurrentDasa8Levels(Time birthTime, Time currentTime)
        {
            //get dasa planet at birth
            var moonConstellation = Calculate.PlanetConstellation(PlanetName.Moon, birthTime);
            var birthDasaPlanetMoon = ConstellationDasaPlanet(moonConstellation.GetConstellationName());

            //get time traversed in birth dasa 
            var timeTraversedInDasa = YearsTraversedInBirthDasa(moonConstellation, birthTime);

            //get time from birth to current time 
            var timeBetween = currentTime.Subtract(birthTime).TotalDays / Calculate.SolarYearTimeSpan;

            //combine years traversed at birth and years to current time
            var combinedYears = timeTraversedInDasa + timeBetween;
            var wholeDasa = DasaCountedFromInputDasa(birthDasaPlanetMoon, combinedYears);

            return wholeDasa;
        }

        /// <summary>
        /// Gets next planet in Ashtottari Dasa order
        /// </summary>
        public static PlanetName NextDasaPlanet(PlanetName planet)
        {
            if (planet == Library.PlanetName.Sun) { return Library.PlanetName.Moon; }
            if (planet == Library.PlanetName.Moon) { return Library.PlanetName.Mars; }
            if (planet == Library.PlanetName.Mars) { return Library.PlanetName.Mercury; }
            if (planet == Library.PlanetName.Mercury) { return Library.PlanetName.Jupiter; }
            if (planet == Library.PlanetName.Jupiter) { return Library.PlanetName.Venus; }
            if (planet == Library.PlanetName.Venus) { return Library.PlanetName.Saturn; }
            if (planet == Library.PlanetName.Saturn) { return Library.PlanetName.Rahu; }
            if (planet == Library.PlanetName.Rahu) { return Library.PlanetName.Sun; }

            throw new Exception("Planet not found!");
        }

        /// <summary>
        /// Gets the full Dasa years for a given planet in Ashtottari system
        /// </summary>
        public static double PD1PlanetFullYears(PlanetName planet)
        {
            if (planet == Library.PlanetName.Sun) { return 6.0; }
            if (planet == Library.PlanetName.Moon) { return 10.0; }
            if (planet == Library.PlanetName.Mars) { return 7.0; }
            if (planet == Library.PlanetName.Mercury) { return 17.0; }
            if (planet == Library.PlanetName.Jupiter) { return 16.0; }
            if (planet == Library.PlanetName.Venus) { return 20.0; }
            if (planet == Library.PlanetName.Saturn) { return 19.0; }
            if (planet == Library.PlanetName.Rahu) { return 13.0; }

            throw new Exception("Planet not found!");
        }

        /// <summary>
        /// Gets the full years of a bhukti planet in a dasa
        /// </summary>
        public static double PD2PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet)
        {
            //108 years is the total of all the dasa planet's years in Ashtottari
            const double fullHumanLifeYears = 108.0;

            //the time a bhukti planet consumes in a dasa is
            //a fixed percentage it consumes in a person's full life
            var bhuktiPlanetPercentage = PD1PlanetFullYears(pd2Planet) / fullHumanLifeYears;

            //bhukti planet's years in a dasa is percentage of the dasa planet's full years
            var bhuktiPlanetFullYears = bhuktiPlanetPercentage * PD1PlanetFullYears(pd1Planet);

            return bhuktiPlanetFullYears;
        }

        /// <summary>
        /// Gets the full years of an antaram planet in a bhukti of a dasa
        /// </summary>
        public static double PD3PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet, PlanetName pd3Planet)
        {
            //108 years is the total of all the dasa planet's years in Ashtottari
            const double fullHumanLifeYears = 108.0;

            //the time an antaram planet consumes in a bhukti is
            //a fixed percentage it consumes in a person's full life
            var antaramPlanetPercentage = PD1PlanetFullYears(pd3Planet) / fullHumanLifeYears;

            //Antaram planet's full years is a percentage of the Bhukti planet's full years
            var antaramPlanetFullYears = antaramPlanetPercentage * PD2PlanetFullYears(pd1Planet, pd2Planet);

            return antaramPlanetFullYears;
        }

        /// <summary>
        /// Gets the full time of an Sukshma planet
        /// </summary>
        public static double PD4PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet, PlanetName pd3Planet, PlanetName pd4Planet)
        {
            const double fullHumanLifeYears = 108.0;
            var sukshmaPlanetPercentage = PD1PlanetFullYears(pd4Planet) / fullHumanLifeYears;
            var sukshmaPlanetFullYears = sukshmaPlanetPercentage * PD3PlanetFullYears(pd1Planet, pd2Planet, pd3Planet);
            return sukshmaPlanetFullYears;
        }

        /// <summary>
        /// Gets the full time of a Prana planet
        /// </summary>
        public static double PD5PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet, PlanetName pd3Planet, PlanetName pd4Planet, PlanetName pd5Planet)
        {
            const double fullHumanLifeYears = 108.0;
            var pd5PlanetPercentage = PD1PlanetFullYears(pd5Planet) / fullHumanLifeYears;
            var pd5PlanetFullTime = pd5PlanetPercentage * PD4PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet);
            return pd5PlanetFullTime;
        }

        /// <summary>
        /// Gets the full time of an Avi Prana planet
        /// </summary>
        public static double PD6PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet, PlanetName pd3Planet, PlanetName pd4Planet, PlanetName pd5Planet, PlanetName pd6Planet)
        {
            const double fullHumanLifeYears = 108.0;
            var pd6PlanetPercentage = PD1PlanetFullYears(pd6Planet) / fullHumanLifeYears;
            var pd6PlanetFullTime = pd6PlanetPercentage * PD5PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet);
            return pd6PlanetFullTime;
        }

        /// <summary>
        /// Gets the full time of a Viprana planet
        /// </summary>
        public static double PD7PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet, PlanetName pd3Planet, PlanetName pd4Planet, PlanetName pd5Planet, PlanetName pd6Planet, PlanetName pd7Planet)
        {
            const double fullHumanLifeYears = 108.0;
            var pd7PlanetPercentage = PD1PlanetFullYears(pd7Planet) / fullHumanLifeYears;
            var pd7PlanetFullTime = pd7PlanetPercentage * PD6PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet, pd6Planet);
            return pd7PlanetFullTime;
        }

        /// <summary>
        /// Gets the full time of a Viprana planet
        /// </summary>
        public static double PD8PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet, PlanetName pd3Planet, PlanetName pd4Planet, PlanetName pd5Planet, PlanetName pd6Planet, PlanetName pd7Planet, PlanetName pd8Planet)
        {
            const double fullHumanLifeYears = 108.0;
            var pd8PlanetPercentage = PD1PlanetFullYears(pd8Planet) / fullHumanLifeYears;
            var pd8PlanetFullTime = pd8PlanetPercentage * PD7PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet, pd6Planet, pd7Planet);
            return pd8PlanetFullTime;
        }

        /// <summary>
        /// Gets the time in years traversed in Dasa at birth
        /// </summary>
        public static double YearsTraversedInBirthDasa(Constellation startConstellation, Time birthTime)
        {
            //get the constellation's quarter
            var quarter = startConstellation.GetQuarter();

            //get the dasa planet for the constellation
            var dasaPlanet = ConstellationDasaPlanet(startConstellation.GetConstellationName());

            //get full years of the dasa planet
            var fullYears = PD1PlanetFullYears(dasaPlanet);

            //calculate years traversed based on quarter
            //each quarter represents 1/4 of the dasa period
            var yearsTraversed = (quarter - 1) * (fullYears / 4.0);

            return yearsTraversed;
        }

        /// <summary>
        /// Gets the dasa planet for a given constellation in Ashtottari system
        /// </summary>
        public static PlanetName ConstellationDasaPlanet(ConstellationName constellationName)
        {
            switch (constellationName)
            {
                case ConstellationName.Aswini:
                case ConstellationName.Magha:
                case ConstellationName.Moola:
                    return Library.PlanetName.Sun;

                case ConstellationName.Bharani:
                case ConstellationName.Poorvashada:
                case ConstellationName.Pubba:
                    return Library.PlanetName.Moon;

                case ConstellationName.Krithika:
                case ConstellationName.Uttarashada:
                case ConstellationName.Uttara:
                    return Library.PlanetName.Mars;

                case ConstellationName.Rohini:
                case ConstellationName.Sravana:
                case ConstellationName.Hasta:
                    return Library.PlanetName.Mercury;

                case ConstellationName.Mrigasira:
                case ConstellationName.Dhanishta:
                case ConstellationName.Chitta:
                    return Library.PlanetName.Jupiter;

                case ConstellationName.Aridra:
                case ConstellationName.Satabhisha:
                case ConstellationName.Swathi:
                    return Library.PlanetName.Venus;

                case ConstellationName.Punarvasu:
                case ConstellationName.Poorvabhadra:
                case ConstellationName.Vishhaka:
                    return Library.PlanetName.Saturn;

                case ConstellationName.Pushyami:
                case ConstellationName.Uttarabhadra:
                case ConstellationName.Anuradha:
                    return Library.PlanetName.Rahu;

                case ConstellationName.Aslesha:
                case ConstellationName.Revathi:
                case ConstellationName.Jyesta:
                    return Library.PlanetName.Sun;
            }

            throw new Exception("Dasa planet for constellation not found!");
        }

        /// <summary>
        /// Counts from inputed dasa by years to dasa, bhukti & antaram
        /// </summary>
        public static Dasas DasaCountedFromInputDasa(PlanetName startDasaPlanet, double years)
        {
            double pd1Years = years;
            double pd2Years;
            double pd3Years;
            double pd4Years;
            double pd5Years;
            double pd6Years;
            double pd7Years;
            double pd8Years;

            var pd1Planet = GetPD1();
            var pd2Planet = GetPD2();
            var pd3Planet = GetPD3();
            var pd4Planet = GetPD4();
            var pd5Planet = GetPD5();
            var pd6Planet = GetPD6();
            var pd7Planet = GetPD7();
            var pd8Planet = GetPD8();

            return new Dasas()
            {
                PD1 = pd1Planet,
                PD2 = pd2Planet,
                PD3 = pd3Planet,
                PD4 = pd4Planet,
                PD5 = pd5Planet,
                PD6 = pd6Planet,
                PD7 = pd7Planet,
                PD8 = pd8Planet
            };

            PlanetName GetPD1()
            {
                var possibleDasaPlanet = startDasaPlanet;
            MinusPD1Years:
                var dasaPlanetFullYears = PD1PlanetFullYears(possibleDasaPlanet);
                pd1Years -= dasaPlanetFullYears;

                if (pd1Years <= 0)
                {
                    pd2Years = pd1Years + dasaPlanetFullYears;
                    return possibleDasaPlanet;
                }
                else
                {
                    possibleDasaPlanet = NextDasaPlanet(possibleDasaPlanet);
                    goto MinusPD1Years;
                }
            }

            PlanetName GetPD2()
            {
                var possiblePD2Planet = pd1Planet;
            MinusPD2Years:
                var pd2PlanetFullYears = PD2PlanetFullYears(pd1Planet, possiblePD2Planet);
                pd2Years -= pd2PlanetFullYears;

                if (pd2Years <= 0)
                {
                    pd3Years = pd2Years + pd2PlanetFullYears;
                    return possiblePD2Planet;
                }
                else
                {
                    possiblePD2Planet = NextDasaPlanet(possiblePD2Planet);
                    goto MinusPD2Years;
                }
            }

            PlanetName GetPD3()
            {
                var possiblePD3Planet = pd2Planet;
            MinusPD3Years:
                var pd3PlanetFullYears = PD3PlanetFullYears(pd1Planet, pd2Planet, possiblePD3Planet);
                pd3Years -= pd3PlanetFullYears;

                if (pd3Years <= 0)
                {
                    pd4Years = pd3Years + pd3PlanetFullYears;
                    return possiblePD3Planet;
                }
                else
                {
                    possiblePD3Planet = NextDasaPlanet(possiblePD3Planet);
                    goto MinusPD3Years;
                }
            }

            PlanetName GetPD4()
            {
                var possiblePD4Planet = pd3Planet;
            MinusPD4Years:
                var pd4PlanetFullYears = PD4PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, possiblePD4Planet);
                pd4Years -= pd4PlanetFullYears;

                if (pd4Years <= 0)
                {
                    pd5Years = pd4Years + pd4PlanetFullYears;
                    return possiblePD4Planet;
                }
                else
                {
                    possiblePD4Planet = NextDasaPlanet(possiblePD4Planet);
                    goto MinusPD4Years;
                }
            }

            PlanetName GetPD5()
            {
                var possiblePD5Planet = pd4Planet;
            MinusPD5Years:
                var pd5PlanetFullYears = PD5PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, possiblePD5Planet);
                pd5Years -= pd5PlanetFullYears;

                if (pd5Years <= 0)
                {
                    pd6Years = pd5Years + pd5PlanetFullYears;
                    return possiblePD5Planet;
                }
                else
                {
                    possiblePD5Planet = NextDasaPlanet(possiblePD5Planet);
                    goto MinusPD5Years;
                }
            }

            PlanetName GetPD6()
            {
                var possiblePD6Planet = pd5Planet;
            MinusPD6Years:
                var pd6PlanetFullYears = PD6PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet, possiblePD6Planet);
                pd6Years -= pd6PlanetFullYears;

                if (pd6Years <= 0)
                {
                    pd7Years = pd6Years + pd6PlanetFullYears;
                    return possiblePD6Planet;
                }
                else
                {
                    possiblePD6Planet = NextDasaPlanet(possiblePD6Planet);
                    goto MinusPD6Years;
                }
            }

            PlanetName GetPD7()
            {
                var possiblePD7Planet = pd6Planet;
            MinusPD7Years:
                var pd7PlanetFullYears = PD7PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet, pd6Planet, possiblePD7Planet);
                pd7Years -= pd7PlanetFullYears;

                if (pd7Years <= 0)
                {
                    pd8Years = pd7Years + pd7PlanetFullYears;
                    return possiblePD7Planet;
                }
                else
                {
                    possiblePD7Planet = NextDasaPlanet(possiblePD7Planet);
                    goto MinusPD7Years;
                }
            }

            PlanetName GetPD8()
            {
                var possiblePD8Planet = pd7Planet;
            MinusPD8Years:
                var pd8PlanetFullYears = PD8PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet, pd6Planet, pd7Planet, possiblePD8Planet);
                pd8Years -= pd8PlanetFullYears;

                if (pd8Years <= 0)
                {
                    return possiblePD8Planet;
                }
                else
                {
                    possiblePD8Planet = NextDasaPlanet(possiblePD8Planet);
                    goto MinusPD8Years;
                }
            }
        }

        /// <summary>
        /// note: used recursively to generate nested JSON for Dasa
        /// feeds on given allDasaEvents list, till last level
        /// </summary>
        public static JObject GetDasaJson(List<DasaEvent> allDasaEvents, int level, DasaEvent parentDasa = null)
        {
            var parentDasaJson = new JObject();

            //get only events for the current dasa level (type)
            //if not specified than must be 1 level dasa
            var isSpecified = parentDasa != null;
            var dasaEvents = isSpecified
                ? allDasaEvents.FindAll(delegate (DasaEvent dasaEvt)
                {
                    var levelMatch = dasaEvt.DasaLevel == level;
                    var parentMatch = dasaEvt.ParentLord == parentDasa.Lord;

                    //make sure sub dasa are within parent dasa time period (before end of parent)
                    var withinTime = dasaEvt.EndTime.GetStdDateTimeOffset() <= parentDasa.EndTime.GetStdDateTimeOffset();

                    return levelMatch && parentMatch && withinTime;
                })
                : allDasaEvents.FindAll(dasaEvt => dasaEvt.DasaLevel == level);

            //if no events found then max level reached
            if (!dasaEvents.Any()) { return null; }

            foreach (var evt in dasaEvents)
            {
                var dasaDataJson = new JObject
                {
                    { "Type", evt.DasaName },
                    { "Start", evt.StartTime.GetStdDateTimeOffsetText() },
                    { "End", evt.EndTime.GetStdDateTimeOffsetText() },
                    { "DurationHours", evt.Duration },
                    { "DurationText", Tools.TimeDurationToHumanText(evt.Duration) },
                    { "TechnicalName", evt.SourceEvent.Name.ToString() },
                    { "Lord", evt.Lord.ToString() },
                    { "ParentLord", evt.ParentLord.ToString() },
                    { "Description", evt.Description },
                    { "Nature", evt.Nature.ToString() }
                };

                //make the sub dasa data (+1 level down) (will be null once last PD level)
                var subDasaJson = GetDasaJson(allDasaEvents, level + 1, evt);

                //if null means this last PD level, so no more sub dasas
                if (subDasaJson != null) { dasaDataJson.Add("SubDasas", subDasaJson); }

                //place nicely in bigger "SubDasas" object for caller
                parentDasaJson[evt.Lord.ToString()] = dasaDataJson;
            }

            return parentDasaJson;
        }
    }
} 