using System;
using System.Collections.Generic;
using System.Linq;

namespace VedAstro.Library
{
    public class ShatabdikaDasa : BaseDasaSystem
    {
        protected override double GetTotalYears()
        {
            return 100.0; // Total duration of Shatabdika dasa
        }

        protected override Dictionary<PlanetName, double> GetPlanetYears()
        {
            return new Dictionary<PlanetName, double>
            {
                { PlanetName.Sun, 5.0 },
                { PlanetName.Moon, 8.0 },
                { PlanetName.Mars, 7.0 },
                { PlanetName.Mercury, 15.0 },
                { PlanetName.Jupiter, 18.0 },
                { PlanetName.Venus, 20.0 },
                { PlanetName.Saturn, 19.0 },
                { PlanetName.Rahu, 8.0 }
            };
        }

        protected override PlanetName[] GetPlanetSequence()
        {
            return new PlanetName[]
            {
                PlanetName.Sun,
                PlanetName.Moon,
                PlanetName.Mars,
                PlanetName.Mercury,
                PlanetName.Jupiter,
                PlanetName.Venus,
                PlanetName.Saturn,
                PlanetName.Rahu
            };
        }

        protected override Dictionary<ConstellationName, PlanetName> GetConstellationPlanetMap()
        {
            return new Dictionary<ConstellationName, PlanetName>
            {
                { ConstellationName.Aswini, PlanetName.Sun },
                { ConstellationName.Bharani, PlanetName.Moon },
                { ConstellationName.Krithika, PlanetName.Mars },
                { ConstellationName.Rohini, PlanetName.Mercury },
                { ConstellationName.Mrigasira, PlanetName.Jupiter },
                { ConstellationName.Aridra, PlanetName.Venus },
                { ConstellationName.Punarvasu, PlanetName.Saturn },
                { ConstellationName.Pushyami, PlanetName.Rahu },
                { ConstellationName.Aslesha, PlanetName.Sun },
                { ConstellationName.Magha, PlanetName.Moon },
                { ConstellationName.Pubba, PlanetName.Mars },
                { ConstellationName.Uttara, PlanetName.Mercury },
                { ConstellationName.Hasta, PlanetName.Jupiter },
                { ConstellationName.Chitta, PlanetName.Venus },
                { ConstellationName.Swathi, PlanetName.Saturn },
                { ConstellationName.Vishhaka, PlanetName.Rahu },
                { ConstellationName.Anuradha, PlanetName.Sun },
                { ConstellationName.Jyesta, PlanetName.Moon },
                { ConstellationName.Moola, PlanetName.Mars },
                { ConstellationName.Poorvashada, PlanetName.Mercury },
                { ConstellationName.Uttarashada, PlanetName.Jupiter },
                { ConstellationName.Sravana, PlanetName.Venus },
                { ConstellationName.Dhanishta, PlanetName.Saturn },
                { ConstellationName.Satabhisha, PlanetName.Rahu },
                { ConstellationName.Poorvabhadra, PlanetName.Sun },
                { ConstellationName.Uttarabhadra, PlanetName.Moon },
                { ConstellationName.Revathi, PlanetName.Mars }
            };
        }
    }
} 