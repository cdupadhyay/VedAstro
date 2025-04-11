using System;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json.Linq;

namespace VedAstro.Library
{
    public partial class Calculate
    {
        /// <summary>
        /// Calculates dasa periods for a specific time range using the specified dasa system
        /// </summary>
        public static JObject DasaAtRange(Time birthTime, Time startTime, Time endTime, int levels = 4, int precisionHours = 504, DasaType dasaType = DasaType.Vimshottari)
        {
            //set what dasa levels to include based on input level
            var tagList = new List<EventTag>
            {
                //Dasa > Bhukti > Antaram > Sukshma > Prana > Avi Prana > Viprana
                EventTag.PD1, EventTag.PD2, EventTag.PD3, EventTag.PD4,
            };

            // TEMP hack to place time in Person (wrapped) 
            var johnDoe = new Person("", birthTime, Gender.Empty);

            //do calculation (heavy computation)
            List<Event> eventList = EventManager.CalculateEvents(precisionHours,
                                                                startTime,
                                                                endTime,
                                                                johnDoe,
                                                                tagList);

            //convert to Dasa Events
            var dasaEvents = new List<DasaEvent>();
            foreach (var e in eventList)
            {
                //cast to dasa event
                var dasaEvent = new DasaEvent(e);
                dasaEvents.Add(dasaEvent);
            }

            //get dasa JSON based on dasa system
            return dasaType switch
            {
                DasaType.Vimshottari => VimshottariDasa.GetDasaJson(dasaEvents, 1),
                DasaType.Ashtottari => AshtottariDasa.GetDasaJson(dasaEvents, 1),
                _ => throw new ArgumentException($"Dasa system {dasaType} not implemented")
            };
        }
    }
} 