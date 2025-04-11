using System;
using System.Collections.Generic;
using System.Linq;

namespace VedAstro.Library
{
    public class DwisaptatiSamaDasa : BaseDasaSystem
    {
        protected override double GetTotalYears()
        {
            return 72.0; // Total duration of DwisaptatiSama dasa
        }

        protected override Dictionary<PlanetName, double> GetPlanetYears()
        {
            return new Dictionary<PlanetName, double>
            {
                { PlanetName.Sun, 9.0 },
                { PlanetName.Moon, 9.0 },
                { PlanetName.Mars, 9.0 },
                { PlanetName.Mercury, 9.0 },
                { PlanetName.Jupiter, 9.0 },
                { PlanetName.Venus, 9.0 },
                { PlanetName.Saturn, 9.0 },
                { PlanetName.Rahu, 9.0 }
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