<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
-->


<!-- PROJECT LOGO 
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
-->

<h3 align="center">Data Scraping for Glassdoor</h3>

  <p align="center">
    This is python to scrape overview and reviews of companies from Glassdoor. Please use it carefully and follow the Terms of Service that explicitly prohibits web scraping.
  </p>
</div>

### Built With

* Python
* ChromeDriver

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Download the SeleniumGlassdor.py file. Change the path of the chromedriver on your machine. Use your own file that contain the lists of the companies glassdoor url. The company url csv file is also attached here. The way to generate the file is also based on selenium, searching the 'glassdoor' + company name in google search engine, and extract the url from the first results. Per requests, I can also upload the file accordingly.

### Prerequisites

Install the selenium before using it.
* selenium
  ```sh
  pip install selenium
  ```

## For the other sections
If you want to scape data from the other sections, such as jobs, salaries. You can use the following methods to first extract the url and then use the similar method to downlode the sections.

* reviewsUrl = browser.find_element_by_xpath("//a[@data-label='Reviews']").get_attribute('href')
* jobsUrl = browser.find_element_by_xpath("//a[@data-label='Jobs']").get_attribute('href')
* salariesUrl = browser.find_element_by_xpath("//a[@data-label='Salaries']").get_attribute('href')
* interviewsUrl = browser.find_element_by_xpath("//a[@data-label='Inter­views']").get_attribute('href')
* benefitsUrl = browser.find_element_by_xpath("//a[@data-label='Benefits']").get_attribute('href')
* photosUrl = browser.find_element_by_xpath("//a[@data-label='Photos']").get_attribute('href')

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Houping - hxiao@gsu.edu

<p align="right">(<a href="#top">back to top</a>)</p>


<p align="right">(<a href="#top">back to top</a>)</p>
