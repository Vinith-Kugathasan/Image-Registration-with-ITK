# Image-Registration-with-ITK
This repository contains implementation of a python script to perform image registration on two MRI volumes of different contrast. ITK was used to implement the registration framework and 3D Slicer was used for performance evaluation. Registration framework consists of three distinct components namely, transform, metric and optimizer. For each element, appropriate function was selected based on theoretical explanation and trial-and-error analysis.

## Implementation
The considered MRI volumes are of 2 different MRI modalities, namely T2-Weighted MRI and T1-Weighted MRI. For the task of registration,T1-Weighted MRI volume is used as the Fixed Image to which T2-Weighted MRI volume (Moving Image) is registered. 

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
- Metric : itk.MattesMutualInformationImageToImageMetricv4
```
```
- Optimizer : itk.RegularStepGradientDescentOptimizerv4
```
```
- Registration : itk.ImageRegistrationMethodv4
```
```