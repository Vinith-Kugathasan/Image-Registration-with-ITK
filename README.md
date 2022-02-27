# Image-Registration-with-ITK
This repository contains implementation of a python script to perform image registration on two MRI volumes of different contrasts. ITK is used to implement the registration framework and 3D Slicer is used for performance evaluation. Registration framework consists of four distinct components namely, transform, metric, interpolator and optimizer. For each element, appropriate function was selected based on theoretical explanation and trial-and-error analysis.

Image Registration Framework (Colab): 
[![Open In Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1UJdb0eVk-lEVkqC6iriCei44O4tMYItt#scrollTo=6Pk4pRHRugXq)

## Implementation
The considered MRI volumes are of 2 different MRI modalities, namely T1-Weighted MRI and T2-Weighted MRI. For the task of registration,T1-Weighted MRI volume is used as the Fixed Image to which T2-Weighted MRI volume (Moving Image) is registered. 

                        Fixed Image                                         Moving Image

<img src="https://github.com/Vinith-Kugathasan/Image-Registration-with-ITK/blob/main/Images/fixed_image.gif" width="400"/> <img src="https://github.com/Vinith-Kugathasan/Image-Registration-with-ITK/blob/main/Images/moving_image.gif" width="400"/>

### Registration Framework
Following are the components and the corresponding functions utilized for the implemented registration framework.

- Transform : itk.TranslationTransform
```
TransformType = itk.TranslationTransform[itk.D, Dimension]
initialTransform = TransformType.New()

movingInitialTransform = TransformType.New()
initialParameters = movingInitialTransform.GetParameters()
initialParameters[0] = 0
initialParameters[1] = 0
movingInitialTransform.SetParameters(initialParameters)

identityTransform = TransformType.New()
identityTransform.SetIdentity()
```
- Interopolator : itk.LinearInterpolateImageFunction
```
interpolator = itk.LinearInterpolateImageFunction[FixedImageType,itk.D]
```
- Metric : itk.MattesMutualInformationImageToImageMetricv4
```
MetricType = itk.MattesMutualInformationImageToImageMetricv4[FixedImageType, MovingImageType]
metric = MetricType.New()

numberOfBins = 24
metric.SetNumberOfHistogramBins(numberOfBins)
metric.SetUseMovingImageGradientFilter(False)
metric.SetUseFixedImageGradientFilter(False)
metric.SetFixedInterpolator(interpolator.New())
metric.SetMovingInterpolator(interpolator.New())
```
- Optimizer : itk.RegularStepGradientDescentOptimizerv4
```
optimizer = itk.RegularStepGradientDescentOptimizerv4.New(LearningRate = 4, MinimumStepLength = 0.001, RelaxationFactor = 0.5, NumberOfIterations = 200)
```
- Registration : itk.ImageRegistrationMethodv4
```
registration = itk.ImageRegistrationMethodv4[FixedImageType, MovingImageType].New(FixedImage = fixedImage, MovingImage = movingImage, Metric = metric, Optimizer = optimizer, InitialTransform = initialTransform)

registration.SetMovingInitialTransform(movingInitialTransform)
registration.SetFixedInitialTransform(identityTransform)

registration.SetNumberOfLevels(1)
registration.SetSmoothingSigmasPerLevel([0])
registration.SetShrinkFactorsPerLevel([1])
```

### Optimization
```
python .\itk_registration.py .\Data\VF-MRT1-1014-1174.vtk .\Data\VF-MRT2-1014-1174.vtk .\Data\
```
![Optimizer update.jpg](Images/Optimizer_update.jpg)
![Metric vs iterations.png](Images/Metric_vs_iter.png)
![Translations vs iterations.png](Images/Translations_vs_iter.png)

### Visualization of Results
![Output comparison.png](Images/Output_comparison.png)
![Composite output comparison 1.png](Images/Composite_output_comparison_1.png)
![Composite output comparison 2.png](Images/Composite_output_comparison_2.png)
![Composite output comparison 3.png](Images/Composite_output_comparison_3.png)

                    Before Registration                                      After Registration

<img src="https://github.com/Vinith-Kugathasan/Image-Registration-with-ITK/blob/main/Images/before_registration_image.gif" width="400"/> <img src="https://github.com/Vinith-Kugathasan/Image-Registration-with-ITK/blob/main/Images/after_registration_image.gif" width="400"/>

<img src="https://github.com/Vinith-Kugathasan/Image-Registration-with-ITK/blob/main/Images/before_registration_image%20(1).gif" width="400"/> <img src="https://github.com/Vinith-Kugathasan/Image-Registration-with-ITK/blob/main/Images/after_registration_image%20(1).gif" width="400"/>

### Slicer 3D Analysis
#### Fixed Image vs Moving Image
![Fixed vs Moving.jpg](Images/Fixed_vs_moving.jpg)
#### Fixed Image vs Registered Image
![Fixed vs Registered.jpg](Images/Fixed_vs_Registered.jpg)
#### Moving Image vs Registered Image
![Moving vs Registered.jpg](Images/Moving_vs_Registered.jpg)

### More Qualitative Comparisons
![Output comparison 2.png](Images/Output_comparison_2.png)
![Output comparison 3.png](Images/Output_comparison_3.png)
![Output comparison 4.png](Images/Output_comparison_4.png)
![Output comparison 5.png](Images/Output_comparison_5.png)
![Output comparison 6.png](Images/Output_comparison_6.png)
![Output comparison 7.png](Images/Output_comparison_7.png)