from rest_framework import serializers

def validate_len(value):
    '''
    Restrict title length to max lenth of 50
    '''
    if len(value) > 50:
        raise serializers.ValidationError(f"`{value}` exceeds the {len(value)} character")
    return value
