def test_setup(smbus2, ioexpander):
    import encoderwheel
    encoder = encoderwheel.EncoderWheel()

    ioexpander.encoder.Encoder.assert_called_once_with(
        encoder.ioe,
        encoder.ENC_CHANNEL,
        encoder.ENC_TERMS,
        count_microsteps=True,
        count_divider=2
    )
