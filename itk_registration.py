import sys
import itk

if len(sys.argv) != 4:
    print("Usage: " + sys.argv[0] + " <fixedImageFile> <movingImageFile> <outputPath>")
    sys.exit(1)

fixedImageFile = sys.argv[1]
movingImageFile = sys.argv[2]
outputImageFile = sys.argv[3] + "/registered.vtk"
differenceImageAfterFile = sys.argv[3] + "/difference_after.vtk" 
differenceImageBeforeFile = sys.argv[3] + "/difference_before.vtk"


PixelType = itk.F

fixedImage = itk.imread(fixedImageFile, PixelType)
movingImage = itk.imread(movingImageFile, PixelType)

Dimension = fixedImage.GetImageDimension()
FixedImageType = itk.Image[PixelType, Dimension]
MovingImageType = itk.Image[PixelType, Dimension]

print(f"Fixed Image Shape : {fixedImage.shape}")
print(f"Moving Image Shape : {movingImage.shape}")
print(f"Dimension : {Dimension}")

# Transform
TransformType = itk.TranslationTransform[itk.D, Dimension]
initialTransform = TransformType.New()

movingInitialTransform = TransformType.New()
initialParameters = movingInitialTransform.GetParameters()
initialParameters[0] = 0
initialParameters[1] = 0
movingInitialTransform.SetParameters(initialParameters)

identityTransform = TransformType.New()
identityTransform.SetIdentity()

# Interpolator
# interpolator = itk.NearestNeighborInterpolateImageFunction[FixedImageType,itk.D]
interpolator = itk.LinearInterpolateImageFunction[FixedImageType,itk.D]

# Metric
# metric = itk.MeanSquaresImageToImageMetricv4[FixedImageType, MovingImageType].New()
metric = itk.MattesMutualInformationImageToImageMetricv4[FixedImageType, MovingImageType].New()

numberOfBins = 24
metric.SetNumberOfHistogramBins(numberOfBins)
metric.SetUseMovingImageGradientFilter(False)
metric.SetUseFixedImageGradientFilter(False)
metric.SetFixedInterpolator(interpolator.New())
metric.SetMovingInterpolator(interpolator.New())

# Optimizer
optimizer = itk.RegularStepGradientDescentOptimizerv4.New(LearningRate=4, MinimumStepLength=0.001, RelaxationFactor=0.5, NumberOfIterations=200)

# Registation
registration = itk.ImageRegistrationMethodv4[FixedImageType, MovingImageType].New(FixedImage=fixedImage, MovingImage=movingImage, Metric=metric, Optimizer=optimizer, InitialTransform=initialTransform)

registration.SetMovingInitialTransform(movingInitialTransform)
registration.SetFixedInitialTransform(identityTransform)

registration.SetNumberOfLevels(1)
registration.SetSmoothingSigmasPerLevel([0])
registration.SetShrinkFactorsPerLevel([1])

# registration.SetNumberOfLevels(2)
# registration.SetSmoothingSigmasPerLevel([0, 0])
# registration.SetShrinkFactorsPerLevel([1, 2])

# registration.SetNumberOfLevels(3)
# registration.SetSmoothingSigmasPerLevel([0, 0, 0])
# registration.SetShrinkFactorsPerLevel([1, 2, 3])

params = []
def iterationUpdate():
    transform = registration.GetTransform()
    currentParameter = transform.GetParameters()
    params.append([optimizer.GetCurrentIteration(), optimizer.GetValue(), currentParameter.GetElement(0), currentParameter.GetElement(1), currentParameter.GetElement(2)])
    print(
        "Iter: %i --> Metric: %f   Translation X: %f, Translation Y: %f, Translation Z: %f"
        % (
            optimizer.GetCurrentIteration(),
            optimizer.GetValue(),
            currentParameter.GetElement(0),
            currentParameter.GetElement(1),
            currentParameter.GetElement(2)
        )
    )


iterationCommand = itk.PyCommand.New()
iterationCommand.SetCommandCallable(iterationUpdate)
optimizer.AddObserver(itk.IterationEvent(), iterationCommand)

registration.Update()

transform = registration.GetTransform()
finalParameters = transform.GetParameters()
translationAlongX = finalParameters.GetElement(0)
translationAlongY = finalParameters.GetElement(1)
translationAlongZ = finalParameters.GetElement(2)

numberOfIterations = optimizer.GetCurrentIteration()

bestValue = optimizer.GetValue()

params.append([optimizer.GetCurrentIteration(), optimizer.GetValue(), finalParameters.GetElement(0), finalParameters.GetElement(1), finalParameters.GetElement(2)])


print("Result = ")
print(" Translation X = " + str(translationAlongX))
print(" Translation Y = " + str(translationAlongY))
print(" Translation Z = " + str(translationAlongZ))
print(" Iterations    = " + str(numberOfIterations))
print(" Metric value  = " + str(bestValue))


CompositeTransformType = itk.CompositeTransform[itk.D, Dimension]
outputCompositeTransform = CompositeTransformType.New()
outputCompositeTransform.AddTransform(movingInitialTransform)
outputCompositeTransform.AddTransform(registration.GetModifiableTransform())

resampler = itk.ResampleImageFilter.New(Input=movingImage, Transform=outputCompositeTransform, UseReferenceImage=True, ReferenceImage=fixedImage)
resampler.SetDefaultPixelValue(100)


OutputPixelType = itk.UC
OutputImageType = itk.Image[OutputPixelType, Dimension]
caster = itk.CastImageFilter[FixedImageType,OutputImageType].New(Input=resampler)
caster_3d = caster.GetOutput()

OutputPixelType = itk.F
OutputImageType = itk.Image[OutputPixelType, Dimension]

writer = itk.ImageFileWriter.New(Input = resampler, FileName = outputImageFile)
writer.SetFileName(outputImageFile)
writer.Update()

out_3d = resampler.GetOutput()

difference = itk.SubtractImageFilter.New(Input1=fixedImage, Input2=resampler)
intensityRescaler = itk.RescaleIntensityImageFilter[FixedImageType, OutputImageType].New(Input=difference, OutputMinimum=itk.NumericTraits[OutputPixelType].min(),
            OutputMaximum=itk.NumericTraits[OutputPixelType].max())


resampler.SetDefaultPixelValue(1)
writer.SetInput(intensityRescaler.GetOutput())
writer.SetFileName(differenceImageAfterFile)
writer.Update()
after_diff = intensityRescaler.GetOutput()

resampler_2 = itk.ResampleImageFilter.New(Input=movingImage, Transform=identityTransform, UseReferenceImage=True, ReferenceImage=fixedImage)
difference_2 = itk.SubtractImageFilter.New(Input1=fixedImage, Input2=resampler_2)
intensityRescaler_2 = itk.RescaleIntensityImageFilter[FixedImageType, OutputImageType].New(Input=difference_2, OutputMinimum=itk.NumericTraits[OutputPixelType].min(),
            OutputMaximum=itk.NumericTraits[OutputPixelType].max())
before_diff = intensityRescaler_2.GetOutput()

writer.SetInput(intensityRescaler_2.GetOutput())
writer.SetFileName(differenceImageBeforeFile)
writer.Update()