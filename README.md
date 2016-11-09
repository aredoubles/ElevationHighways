
# Highway elevations

### Plotting the elevations of interstate highways across the USA

I recently moved from Austin, TX to Boston, MA. It was a four-day drive!

At one point, I found myself on Interstate 80, somewhere in eastern Pennsylvania (actually I don't remember exactly, the whole long trip is a blur).

As the highway crested over a mountain pass in the Appalachians, I was struck by the text on a highway sign.

![I80Sign](https://upload.wikimedia.org/wikipedia/commons/3/3e/I80_Highest_Point.jpg)

Apparently, I had just crested the highest point on this highway's Eastern section. The next time the highway would reach a similar elevation would be somewhere in Wyoming. I don't remember the exact details (I just found this example image on Wikipedia), but I do remember being momentarily awed, by the long scales of these highways, and the perspectives that are needed to sense those scales.

And for some reason, it reminded me of the album cover for '*Unknown Pleasures*', by Joy Division.

![UnknownPleasures](https://upload.wikimedia.org/wikipedia/en/7/70/Unknown_Pleasures_Joy_Division_LP_sleeve.jpg)

It's an incredibly famous album cover, with [fascinating origins](https://blogs.scientificamerican.com/sa-visual/pop-culture-pulsar-origin-story-of-joy-division-s-unknown-pleasures-album-cover-video/).

![Pulsars](https://blogs.scientificamerican.com/blogs/assets/sa-visual/Image/pulsar_trio.jpg)

I thought: wouldn't it be cool to plot the elevations of interstate highways, and then stack them on top of each other, à la *Unknown Pleasures*? Such an image would present a cross-sectional slice of America, as experienced by drivers on interstate highways, but on a scale greater than what we might usually sense.

Another source of inspiration is John McPhee's classic book [*Annals of the Former World*](https://en.wikipedia.org/wiki/Annals_of_the_Former_World), which describes American geology across I-80. It's one of my favorite books. His choice of I-80 is somewhat arbitrary, and so this project could also be a simple glimpse into what other highways might present geologically.

And so this project was born!

## Workflow

* Find the routes of cross-country interstate highways in the USA
    * The Google Maps API can find Directions, and I can use that (plus waypoint adjustments) to get the routes of highways
    * Alternatively, find KML files that precisely trace highway routes
* Encode these routes in a compressed format
    * Google's [Polyline algorithm](https://developers.google.com/maps/documentation/utilities/polylinealgorithm) is perfect for this!
* Use the Google Maps Elevations API to find the elevations along these highway routes
* Plot those elevations!
* Repeat for all major interstate highways!

## Current progress

* I-40 has been completed! The plot is below.
    * Lots of manual work involved though
        * Routing done manually (though see Todo below)

![I-40 Plot](I40plot.png)

## Todo

* Wikipedia actually has KML files for these highways!
    * Way more precise than my manual routing!
    * But since the Google Elevations API still requires coordinates or polylines, is there a simple way to convert KML? Preferably in Python.
* Add more highways, of course
* My Google Maps API key is currently made public, which is certainly not good practice, I'll need to import that separately somehow

## Footnotes

* Roger Shaw
* Currently a fellow at Insight Health Data Science, transitioning from academia into a career in data science
* This is just a side project, for playing around with Google Maps APIs, geoegraphic data, nested JSONs, plotting, etc.
