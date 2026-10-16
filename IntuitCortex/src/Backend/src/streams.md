# Available Data Streams for Cortex API
> 'eeg'
- Raw eeg data
{
    + COUNTER:
    > Resets to 0 every second
    > Increment by 1 per sample
    + INTERPOLATED: 
    > 0 = Val From Headset
    > 1 = Interpolated value
    EEG SENSORS: Value in microvolt
    { 
        AF3: Left Frontal Cortex
        T7: Left Temportal Cortex
        Pz: Parietal Cortex
        T8: Right Temportal Cortex
        AF4: Right Frontal Cortex
    }
    RAW_CQ: Raw val of contact quality
    + MARKER_HARDWARE
    > 1 if a marker was recieved for the EEG sample.
    > 0 otherwise
    + MARKERS
    > Array of markers. 
    > Includes markers sent by all the application working with the headset. 
}
Sample EEG Data
{
  "eeg": [
    8,
    0,
    4202.051, 4235.385, 4146.667, 4210.769, 4108.718,
    0,
    0,
    []
  ],
  "sid": "8bbc58bd-0ab1-404e-b472-dac1322dbe5b",
  "time": 1590402103.9016
}
> 'mot'
- Motion data
> 'dev'
- Battery level, wireless signal strength, and contact quality
> 'eq'
- EEG quality of each sensor
> 'pow'
- Band power of each sensor
- Alpha, low beta, high beta, gamma, and theta bands
[
    "AF3/theta","AF3/alpha","AF3/betaL","AF3/betaH","AF3/gamma",
    "T7/theta","T7/alpha","T7/betaL","T7/betaH","T7/gamma",
    "Pz/theta","Pz/alpha","Pz/betaL","Pz/betaH","Pz/gamma",
    "T8/theta","T8/alpha","T8/betaL","T8/betaH","T8/gamma",
    "AF4/theta","AF4/alpha","AF4/betaL","AF4/betaH","AF4/gamma"
]
Sample Band Power 
{
  "pow": [
    1.246,0.706,0.566,1.065,0.602,
    10.293,4.374,11.638,351.767,40.273,
    50.159,4.585,0.467,1.481,3.764,
    9.861,3.139,2.094,3.342,4.452,
    75.652,1.972,2.932,2.555,7.005
  ],
  "sid": "ff0245d1-9531-424c-9f6d-9f736f465516",
  "time": 1590403491.0307
}
> 'met'
- Performance Metrics
> 'com'
- Results of mental commands detection
> 'fac'
- Facial Expressions
> 'sys'
- System events