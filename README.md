**FZStats: FocalZonalStatistics**
====
## 1. Preface
Spatial Position Dependence (SPD) and Spatial Stratified Heterogeneity (SSH) are two important characteristics of spatial data. Current spatial statistical toolbox include tools for modeling either SPD or SSH, such as the Focal Statistics and Zonal Statistics tool modules provided by mainstream GIS software like ArcGIS. However, SPD and SSH often coexist in practice, creating a need for basic spatial statistical methods that can simultaneously address both. This is the motivation behind the development of the Focal-Zonal Mixed Statistics method.

The new developed toolbox FZStats V1.0 integrating the traditional Focal Statistics and Zonal Statistics methods, while introducing the Focal-Zonal Mixed Statistics method, which simultaneously addresses spatial dependence and stratified heterogeneity. This toolbox is applicable to a variety of scenarios, such as potential estimation, geological anomaly analysis, and spatial filtering, providing researchers with more accurate analytical results. The toolbox offers the following features:
- It includes not only the new Focal-Zonal Mixed Statistics method but also the traditional Focal Statistics and Zonal Statistics, allowing users to choose the most suitable method based on their objectives and application scenarios.
- The new method Focal-zonal Mixed statistics merges the functionalities of traditional Focal and Zonal Statistics to handle both spatial stratified heterogeneity and spatial dependence simultaneously.
- It supports elliptical neighborhood windows, expanding the types of neighborhood windows available.
- It allows the calculation of various statistics, including the coefficient of variation.
- It provides data chunking capabilities to reduce memory load and simplify large-scale data processing.
- It supports multiprocessing to improve statistical efficiency.
- By setting a minimum sample threshold, the reliability of statistical results is enhanced.
- It supports batch processing of statistical tasks, simplifying parameter configuration and improving work efficiency.

## 2. Installation and Startup
FZStats V1.0 requires no installation and is a portable software toolbox. Users can directly use the toolbox by double-clicking the “FocalZonalStatisticsMain.exe” application (the latest version is available via the following link: https://zenodo.org/records/13208114). The toolbox is lightweight and enhances usability and efficiency, making it ideal for researchers and engineers.

## 3. User Interface and Module Description
The main interface of FZStats V1.0 includes three tabs corresponding to the three statistical methods: Focal Statistics, Zonal Statistics, and Focal-Zonal Mixed Statistics. Since Focal-Zonal Mixed Statistics is much more advanced than the other two, and in fact, it encompasses all the settings of both Focal Statistics and Zonal Statistics, we will only introduce Focal-Zonal Mixed Statistics here.

The newly proposed Focal-Zonal Mixed Statistics method ingeniously combines the features of Zonal Statistics and Focal Statistics, allowing statistical analysis to be performed within a local window based on the zones to which each cell belongs. This method not only develops and expands upon traditional methods but can also be seen as a generalization of them:
- When the window is infinitely large, this method becomes equivalent to Zonal Statistics.
- When there is only one zone in the analysis area, it simplifies to traditional Focal Statistics.

The FZ Mixed Stats tab in the FZStats V1.0 tool provides the interface for configuring parameters for Focal-Zonal Mixed Statistics, including the following modules:

#### (1) Input and Output Data Settings (Rasters Setting)

Similar to Zonal Statistics, this method requires two input raster layers:
- A value raster layer (Value Raster) for processing.
- A zone raster layer (Zone Raster) that defines the zones.

Users also need to specify the storage path and file name of the result raster layer (Result Raster), which will store the statistical results.

#### (2) Neighborhood Parameter Settings (Neighbourhood Setting)

Similar to Focal Statistics, this method provides three neighborhood window options:
- **Rectangle (RECTANGLE)**: Defined by half-length and half-width.
- **Circle (CIRCLE)**: Defined by radius.
- **Ellipse (ELLIPSE)**: Defined by the semi-major axis, ratio of the semi-major to semi-minor axis, and rotation angle.

The default neighborhood window is a square with a half-length and half-width of 50 cells.

#### (3) Statistics Type Parameter Settings (Statistics Setting)

Like both Focal Statistics and Zonal Statistics, this method supports the calculation of various statistics, such as: Mean, Percentile, Standard Deviation (STD), Maximum, Minimum, Sum, Median, Variety, Range, Majority, Minority, Cells Count, and Coefficient of Variation.

The default statistic type is Mean.

#### (4) Advanced Settings (Optimization)

Similar to Focal Statistics, this method supports the following optimization features:
- Sub-gridding: Dividing the input raster into multiple small blocks to reduce memory load and improve performance with large datasets.
- Process Number: Setting the number of processors for parallel processing to speed up calculations.
- Threshold: Setting a minimum sample size threshold to ensure that there are enough samples to improve result reliability.
- Ignore NoData: Users can choose whether to ignore NoData values during calculations.

By default, this option is enabled, meaning that only cells with data values within the neighborhood are used for statistical calculations.

Figure 1 shows a typical configuration interface for Focal-Zonal Mixed Statistics. Users can configure the neighborhood parameters, choose the desired statistics type, and adjust performance optimization parameters. In this example, a circular window with a radius of 300 cells is used, and the statistical type is Mean. The parameter settings are detailed as following:

```bash
Value Raster: E:/rn/FZStats/orig_data/LST_STD.tif
Zone Raster: E:/rn/FZStats/orig_data/AS_class.tif
Result Raster: E:/rn/FZStats/result/cir300_mean_fz.tif
Unit: Cell
Neighbourhood Window: Circle
Radius: 300
Statistics Type: Mean
Columns: 2
Rows: 2
Process Number: 16
Threshold: 1
```

<p align="center">
  <img src="https://github.com/Renna11/FocalZonalStatistics/blob/main/docs/source/pics/ReadMe_Fig1.jpg" alt="ReadMe Image" />
</p>

<p align="center">
Figure 1. Focal-Zonal Mixed Statistics Parameter Settings
</p>

## 4. Batch Processing Function
To further improve the efficiency of multi-task processing and achieve a certain degree of automation, FZStats V1.0 provides a batch processing function. Users can define parameters in an INI-format configuration file (config.ini), which simplifies the repetitive configuration process. This feature allows users to set and execute multiple tasks in one operation, supports parameter reuse, and provides error tracking tools.

Users can add the currently configured parameters to the "config.ini" configuration file by clicking the "Add to Config File" button at the bottom of the interface or through the context menu. They can also open the configuration file directly by selecting the "Open Config File" option from the context menu and manually edit the parameters in the specified format. The configuration file format is shown in Figure 2.

<p align="center">
  <img src="https://github.com/Renna11/FocalZonalStatistics/blob/main/docs/source/pics/ReadMe_Fig2.jpg" alt="ReadMe Image" />
</p>

<p align="center">
Figure 2. config.ini Configuration File
</p>

Users can directly run all the statistical tasks in the configuration file by selecting the "Run Config File" option from the context menu. This feature allows users to batch process tasks without repeating manual input, thus improving work efficiency and convenience. Before running the configuration file, make sure that the parameter settings in the file are correct.

## 5. Example
Topographic factors have a significant impact on the identification of geothermal anomalies. Therefore, effectively suppressing the interference of topographic factors is crucial for geothermal anomaly identification. This example uses the Focal-Zonal Mixed Statistics method to identify geothermal anomaly areas. The steps are as follows:

- **Step 1:** Select the input data, including the Landsat 8 surface temperature (LST) remote sensing raster data (LST_STD.tif) and the topographic zoning raster data (AS_class.tif).

- **Step 2:** Set the Focal-Zonal Statistics parameters, including the neighborhood range, statistical type, and performance optimization settings.

    In this example, a circular window with a radius of 240 cells is used as the neighborhood, and the mean (MEAN) and standard deviation (STD) layers are calculated separately. The specific parameter settings are shown in Figure 3.

<div align="center">
  <img src="https://github.com/Renna11/FocalZonalStatistics/blob/main/docs/source/pics/ReadMe_Fig3a.jpg" alt="ReadMe Image" width="40%" />
  <img src="https://github.com/Renna11/FocalZonalStatistics/blob/main/docs/source/pics/ReadMe_Fig3b.jpg" alt="ReadMe Image" width="40%" />
</div>

<div align="center">
(a) Mean (MEAN) Layer&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(b) Standard Deviation (STD) Layer
</div>

<p align="center">
Figure 3. Focal-Zonal Parameter Settings Interface
</p>

- **Step 3:** Click the "Run" button to separately execute the calculations and obtain the mean (MEAN) layer and the standard deviation (STD) layer. One can also first add the parameters for calculating the mean and standard deviation to the "config.ini" configuration file, and then use the "Run Config File" menu option to batch process and generate these two layers.

- **Step 4:** Use the raster calculation tool in ArcMap to compute and generate a raster layer of anomalous temperature distribution that suppresses the effects of topography, as shown in Figure 4.

<p align="center">
  <img src="https://github.com/Renna11/FocalZonalStatistics/blob/main/docs/source/pics/ReadMe_Fig4.jpg" alt="ReadMe Image" />
</p>

<p align="center">
Figure 4. Raster Layer Calculation of Anomalous Temperature Distribution with Topographic Effect Suppression
</p>

- **Step 5:** The anomalous temperature distribution raster generated in Step 4, along with the known spatial distribution of geothermal points, will serve as a basis for evaluating the accuracy of the identification results. It will also help comprehensively assess the model's effectiveness and applicability. Figure 5 shows the spatial distribution of the anomalous temperature raster and known geothermal points.

<p align="center">
  <img src="https://github.com/Renna11/FocalZonalStatistics/blob/main/docs/source/pics/ReadMe_Fig5.jpg" alt="ReadMe Image" />
</p>

<p align="center">
Figure 5. Spatial Distribution of Anomalous Temperature Raster Based on Focal-Zonal Statistics and Known Geothermal Points
</p>

## Appendix
Data in this document can be obtained from https://zenodo.org/records/13766015.








