[
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]


hovertemplate
Parent: data[type=scatter]
Type: string or array of strings
Default: ""

Template string used for rendering the information that appear on hover box. Note that this will override `hoverinfo`. Variables are inserted using %{variable}, for example "y: %{y}". Numbers are formatted using d3-format's syntax %{variable:d3-format}, for example "Price: %{y:$.2f}". https://github.com/d3/d3-3.x-api-reference/blob/master/Formatting.md#d3_format for details on the formatting syntax. Dates are formatted using d3-time-format's syntax %{variable|d3-time-format}, for example "Day: %{2019-01-01|%A}". https://github.com/d3/d3-3.x-api-reference/blob/master/Time-Formatting.md#format for details on the date formatting syntax. The variables available in `hovertemplate` are the ones emitted as event data described at this link https://plot.ly/javascript/plotlyjs-events/#event-data. Additionally, every attributes that can be specified per-point (the ones that are `arrayOk: True`) are available. Anything contained in tag `<extra>` is displayed in the secondary box, for example "<extra>{fullData.name}</extra>". To hide the secondary box completely, use an empty tag `<extra></extra>`.




hoverinfo
Parent: data[type=scatter]
Type: flaglist string. Any combination of "x", "y", "z", "text", "name" joined with a "+" OR "all" or "none" or "skip".
Examples: "x", "y", "x+y", "x+y+z", "all"
Default: "all"

Determines which trace information appear on hover. If `none` or `skip` are set, no information is displayed upon hovering. But, if `none` is set, click and hover events are still fired.






-----

marker
Parent: data[type=scatter]
Type: dict containing one or more of the keys listed below.

    symbol
    Parent: data[type=scatter].marker
    Type: enumerated or array of enumerateds , one of ( "0" | "circle" | "100" | "circle-open" | "200" | "circle-dot" | "300" | "circle-open-dot" | "1" | "square" | "101" | "square-open" | "201" | "square-dot" | "301" | "square-open-dot" | "2" | "diamond" | "102" | "diamond-open" | "202" | "diamond-dot" | "302" | "diamond-open-dot" | "3" | "cross" | "103" | "cross-open" | "203" | "cross-dot" | "303" | "cross-open-dot" | "4" | "x" | "104" | "x-open" | "204" | "x-dot" | "304" | "x-open-dot" | "5" | "triangle-up" | "105" | "triangle-up-open" | "205" | "triangle-up-dot" | "305" | "triangle-up-open-dot" | "6" | "triangle-down" | "106" | "triangle-down-open" | "206" | "triangle-down-dot" | "306" | "triangle-down-open-dot" | "7" | "triangle-left" | "107" | "triangle-left-open" | "207" | "triangle-left-dot" | "307" | "triangle-left-open-dot" | "8" | "triangle-right" | "108" | "triangle-right-open" | "208" | "triangle-right-dot" | "308" | "triangle-right-open-dot" | "9" | "triangle-ne" | "109" | "triangle-ne-open" | "209" | "triangle-ne-dot" | "309" | "triangle-ne-open-dot" | "10" | "triangle-se" | "110" | "triangle-se-open" | "210" | "triangle-se-dot" | "310" | "triangle-se-open-dot" | "11" | "triangle-sw" | "111" | "triangle-sw-open" | "211" | "triangle-sw-dot" | "311" | "triangle-sw-open-dot" | "12" | "triangle-nw" | "112" | "triangle-nw-open" | "212" | "triangle-nw-dot" | "312" | "triangle-nw-open-dot" | "13" | "pentagon" | "113" | "pentagon-open" | "213" | "pentagon-dot" | "313" | "pentagon-open-dot" | "14" | "hexagon" | "114" | "hexagon-open" | "214" | "hexagon-dot" | "314" | "hexagon-open-dot" | "15" | "hexagon2" | "115" | "hexagon2-open" | "215" | "hexagon2-dot" | "315" | "hexagon2-open-dot" | "16" | "octagon" | "116" | "octagon-open" | "216" | "octagon-dot" | "316" | "octagon-open-dot" | "17" | "star" | "117" | "star-open" | "217" | "star-dot" | "317" | "star-open-dot" | "18" | "hexagram" | "118" | "hexagram-open" | "218" | "hexagram-dot" | "318" | "hexagram-open-dot" | "19" | "star-triangle-up" | "119" | "star-triangle-up-open" | "219" | "star-triangle-up-dot" | "319" | "star-triangle-up-open-dot" | "20" | "star-triangle-down" | "120" | "star-triangle-down-open" | "220" | "star-triangle-down-dot" | "320" | "star-triangle-down-open-dot" | "21" | "star-square" | "121" | "star-square-open" | "221" | "star-square-dot" | "321" | "star-square-open-dot" | "22" | "star-diamond" | "122" | "star-diamond-open" | "222" | "star-diamond-dot" | "322" | "star-diamond-open-dot" | "23" | "diamond-tall" | "123" | "diamond-tall-open" | "223" | "diamond-tall-dot" | "323" | "diamond-tall-open-dot" | "24" | "diamond-wide" | "124" | "diamond-wide-open" | "224" | "diamond-wide-dot" | "324" | "diamond-wide-open-dot" | "25" | "hourglass" | "125" | "hourglass-open" | "26" | "bowtie" | "126" | "bowtie-open" | "27" | "circle-cross" | "127" | "circle-cross-open" | "28" | "circle-x" | "128" | "circle-x-open" | "29" | "square-cross" | "129" | "square-cross-open" | "30" | "square-x" | "130" | "square-x-open" | "31" | "diamond-cross" | "131" | "diamond-cross-open" | "32" | "diamond-x" | "132" | "diamond-x-open" | "33" | "cross-thin" | "133" | "cross-thin-open" | "34" | "x-thin" | "134" | "x-thin-open" | "35" | "asterisk" | "135" | "asterisk-open" | "36" | "hash" | "136" | "hash-open" | "236" | "hash-dot" | "336" | "hash-open-dot" | "37" | "y-up" | "137" | "y-up-open" | "38" | "y-down" | "138" | "y-down-open" | "39" | "y-left" | "139" | "y-left-open" | "40" | "y-right" | "140" | "y-right-open" | "41" | "line-ew" | "141" | "line-ew-open" | "42" | "line-ns" | "142" | "line-ns-open" | "43" | "line-ne" | "143" | "line-ne-open" | "44" | "line-nw" | "144" | "line-nw-open" )
    Default: "circle"

    Sets the marker symbol type. Adding 100 is equivalent to appending "-open" to a symbol name. Adding 200 is equivalent to appending "-dot" to a symbol name. Adding 300 is equivalent to appending "-open-dot" or "dot-open" to a symbol name


---
This is the list of Plotly colorscales:
[‘Blackbody’,
‘Bluered’,
‘Blues’,
‘Earth’,
‘Electric’,
‘Greens’,
‘Greys’,
‘Hot’,
‘Jet’,
‘Picnic’,
‘Portland’,
‘Rainbow’,
‘RdBu’,
‘Reds’,
‘Viridis’,
‘YlGnBu’,
‘YlOrRd’]


-----
OVER

hover_name="country", hover_data=data["country"]
hoverinfo: Determines which trace information appear on hover
hovertemplate:will override
            `hoverinfo`
"y: %{y}". Numbers are formatted using
            d3-format's syntax %{variable:d3-format}, for example
            "Price: %{y:$.2f}". https://github.com/d3/d3-3.x-api-
            reference/blob/master/Formatting.md#d3_format for
            details on the formatting syntax. Dates are formatted
            using d3-time-format's syntax %{variable|d3-time-
            format}, for example "Day: %{2019-01-01|%A}"
hovertext:Sets hover text elements associated with each (lon,lat)
            pair or item in `locations`. If a single string, the
            same string appears over all the data points. If an
            array of string, the items are mapped in order to the
            this trace's (lon,lat) or `locations` coordinates. To
            be seen, trace `hoverinfo` must contain a "text" flag.


fill

 customdata
            Assigns extra data each datum. This may be useful when
            listening to hover



CSS color:
                aliceblue, antiquewhite, aqua, aquamarine, azure,
                beige, bisque, black, blanchedalmond, blue,
                blueviolet, brown, burlywood, cadetblue,
                chartreuse, chocolate, coral, cornflowerblue,
                cornsilk, crimson, cyan, darkblue, darkcyan,
                darkgoldenrod, darkgray, darkgrey, darkgreen,
                darkkhaki, darkmagenta, darkolivegreen, darkorange,
                darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,
                darkturquoise, darkviolet, deeppink, deepskyblue,
                dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,
                ghostwhite, gold, goldenrod, gray, grey, green,
                greenyellow, honeydew, hotpink, indianred, indigo,
                ivory, khaki, lavender, lavenderblush, lawngreen,
                lemonchiffon, lightblue, lightcoral, lightcyan,
                lightgoldenrodyellow, lightgray, lightgrey,
                lightgreen, lightpink, lightsalmon, lightseagreen,
                lightskyblue, lightslategray, lightslategrey,
                lightsteelblue, lightyellow, lime, limegreen,
                linen, magenta, maroon, mediumaquamarine,
                mediumblue, mediumorchid, mediumpurple,
                mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,
                mintcream, mistyrose, moccasin, navajowhite, navy,
                oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,
                palevioletred, papayawhip, peachpuff, peru, pink,
                plum, powderblue, purple, red, rosybrown,
                royalblue, saddlebrown, salmon, sandybrown,
                seagreen, seashell, sienna, silver, skyblue,
                slateblue, slategray, slategrey, snow, springgreen,
                steelblue, tan, teal, thistle, tomato, turquoise,
                violet, wheat, white, whitesmoke, yellow,
                yellowgreen