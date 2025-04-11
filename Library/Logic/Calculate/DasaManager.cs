using System;
using System.Collections.Generic;
using System.Linq;

namespace VedAstro.Library
{
    public static class DasaManager
    {
        /// <summary>
        /// Gets the current dasa, bhukti & antaram at inputed time based on the specified dasa system
        /// </summary>
        public static Dasas CurrentDasa8Levels(Time birthTime, Time currentTime, DasaType dasaType)
        {
            return dasaType switch
            {
                DasaType.Vimshottari => VimshottariDasa.CurrentDasa8Levels(birthTime, currentTime),
                DasaType.Ashtottari => AshtottariDasa.CurrentDasa8Levels(birthTime, currentTime),
                _ => throw new ArgumentException($"Dasa system {dasaType} not implemented")
            };
        }

        /// <summary>
        /// Gets the next planet in the dasa sequence for the specified dasa system
        /// </summary>
        public static PlanetName NextDasaPlanet(PlanetName planet, DasaType dasaType)
        {
            return dasaType switch
            {
                DasaType.Vimshottari => VimshottariDasa.NextDasaPlanet(planet),
                DasaType.Ashtottari => AshtottariDasa.NextDasaPlanet(planet),
                _ => throw new ArgumentException($"Dasa system {dasaType} not implemented")
            };
        }

        /// <summary>
        /// Gets the full Dasa years for a given planet in the specified dasa system
        /// </summary>
        public static double PD1PlanetFullYears(PlanetName planet, DasaType dasaType)
        {
            return dasaType switch
            {
                DasaType.Vimshottari => VimshottariDasa.PD1PlanetFullYears(planet),
                DasaType.Ashtottari => AshtottariDasa.PD1PlanetFullYears(planet),
                _ => throw new ArgumentException($"Dasa system {dasaType} not implemented")
            };
        }

        /// <summary>
        /// Gets the full years of a bhukti planet in a dasa for the specified dasa system
        /// </summary>
        public static double PD2PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet, DasaType dasaType)
        {
            return dasaType switch
            {
                DasaType.Vimshottari => VimshottariDasa.PD2PlanetFullYears(pd1Planet, pd2Planet),
                DasaType.Ashtottari => AshtottariDasa.PD2PlanetFullYears(pd1Planet, pd2Planet),
                _ => throw new ArgumentException($"Dasa system {dasaType} not implemented")
            };
        }

        /// <summary>
        /// Gets the full years of an antaram planet in a bhukti of a dasa for the specified dasa system
        /// </summary>
        public static double PD3PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet, PlanetName pd3Planet, DasaType dasaType)
        {
            return dasaType switch
            {
                DasaType.Vimshottari => VimshottariDasa.PD3PlanetFullYears(pd1Planet, pd2Planet, pd3Planet),
                DasaType.Ashtottari => AshtottariDasa.PD3PlanetFullYears(pd1Planet, pd2Planet, pd3Planet),
                _ => throw new ArgumentException($"Dasa system {dasaType} not implemented")
            };
        }

        /// <summary>
        /// Gets the full time of a Sukshma planet for the specified dasa system
        /// </summary>
        public static double PD4PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet, PlanetName pd3Planet, PlanetName pd4Planet, DasaType dasaType)
        {
            return dasaType switch
            {
                DasaType.Vimshottari => VimshottariDasa.PD4PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet),
                DasaType.Ashtottari => AshtottariDasa.PD4PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet),
                _ => throw new ArgumentException($"Dasa system {dasaType} not implemented")
            };
        }

        /// <summary>
        /// Gets the full time of a Prana planet for the specified dasa system
        /// </summary>
        public static double PD5PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet, PlanetName pd3Planet, PlanetName pd4Planet, PlanetName pd5Planet, DasaType dasaType)
        {
            return dasaType switch
            {
                DasaType.Vimshottari => VimshottariDasa.PD5PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet),
                DasaType.Ashtottari => AshtottariDasa.PD5PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet),
                _ => throw new ArgumentException($"Dasa system {dasaType} not implemented")
            };
        }

        /// <summary>
        /// Gets the full time of an Avi Prana planet for the specified dasa system
        /// </summary>
        public static double PD6PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet, PlanetName pd3Planet, PlanetName pd4Planet, PlanetName pd5Planet, PlanetName pd6Planet, DasaType dasaType)
        {
            return dasaType switch
            {
                DasaType.Vimshottari => VimshottariDasa.PD6PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet, pd6Planet),
                DasaType.Ashtottari => AshtottariDasa.PD6PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet, pd6Planet),
                _ => throw new ArgumentException($"Dasa system {dasaType} not implemented")
            };
        }

        /// <summary>
        /// Gets the full time of a Viprana planet for the specified dasa system
        /// </summary>
        public static double PD7PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet, PlanetName pd3Planet, PlanetName pd4Planet, PlanetName pd5Planet, PlanetName pd6Planet, PlanetName pd7Planet, DasaType dasaType)
        {
            return dasaType switch
            {
                DasaType.Vimshottari => VimshottariDasa.PD7PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet, pd6Planet, pd7Planet),
                DasaType.Ashtottari => AshtottariDasa.PD7PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet, pd6Planet, pd7Planet),
                _ => throw new ArgumentException($"Dasa system {dasaType} not implemented")
            };
        }

        /// <summary>
        /// Gets the full time of a Viprana planet for the specified dasa system
        /// </summary>
        public static double PD8PlanetFullYears(PlanetName pd1Planet, PlanetName pd2Planet, PlanetName pd3Planet, PlanetName pd4Planet, PlanetName pd5Planet, PlanetName pd6Planet, PlanetName pd7Planet, PlanetName pd8Planet, DasaType dasaType)
        {
            return dasaType switch
            {
                DasaType.Vimshottari => VimshottariDasa.PD8PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet, pd6Planet, pd7Planet, pd8Planet),
                DasaType.Ashtottari => AshtottariDasa.PD8PlanetFullYears(pd1Planet, pd2Planet, pd3Planet, pd4Planet, pd5Planet, pd6Planet, pd7Planet, pd8Planet),
                _ => throw new ArgumentException($"Dasa system {dasaType} not implemented")
            };
        }

        /// <summary>
        /// Gets the dasa planet for a given constellation in the specified dasa system
        /// </summary>
        public static PlanetName ConstellationDasaPlanet(ConstellationName constellationName, DasaType dasaType)
        {
            return dasaType switch
            {
                DasaType.Vimshottari => VimshottariDasa.ConstellationDasaPlanet(constellationName),
                DasaType.Ashtottari => AshtottariDasa.ConstellationDasaPlanet(constellationName),
                _ => throw new ArgumentException($"Dasa system {dasaType} not implemented")
            };
        }
    }
} 