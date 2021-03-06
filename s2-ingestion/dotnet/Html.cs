using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace dotnet
{
    public static class Html
    {
        static string outputDir = "../output/web";
        
        public static void GenerateHtml(List<Product> products)
        {
            Directory.CreateDirectory(outputDir);

            HtmlByDate.Generate(products);
            HtmlByGridsquare.Generate(products);

            Console.WriteLine("Generating HTML index page...");

            var s = new StringBuilder();

            s.Append(@"<html>
                        <head>
                        <title>Sentinel-2 ARD index</title>
                        <link rel=""stylesheet"" href=""https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.13/semantic.min.css""/>
                        <style>
                            body { display:flex; flex-direction:column; }
                            .content { flex: 1; }
                            footer { text-align: center; }
                        </style>
                        </head>
                        <body>
                        <div class=""content"">
                        <div class=""ui container""> 
                        <br />
                        <h1>Sentinel-2 ARD index</h1>
                        <p>Browse the Sentinel-2 ARD by date or by gridsquare.</p>
                          <ul>
                            <li><a href=""bydate/index.html"">Browse by date</a></li>
                            <li><a href=""bygridsquare/index.html"">Browse by gridsquare</a></li>
                          </ul>
                        </div>
                        </div>
                        </body>
                        </html>
                        ");

            File.WriteAllText(Path.Combine(outputDir, "index.html"), s.ToString());
        }
    }
}