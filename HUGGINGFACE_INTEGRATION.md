# HuggingFace Chatbot Integration Update

## Overview
The chatbot has been successfully updated to use Hugging Face's Inference API with GPT-OSS models instead of OpenAI. The integration includes a comprehensive cybersecurity-focused system prompt designed to help users identify and avoid phishing attacks and scams.

## Changes Made

### 1. New HuggingFace Service (`backend/app/services/huggingface_service.py`)
- **Replaced**: `OpenAIService` with `HuggingFaceService`
- **Features**:
  - Comprehensive cybersecurity system prompt
  - Advanced fraud detection and analysis
  - Risk level assessment (low/medium/high/critical)
  - Fallback responses for API unavailability
  - Enhanced warning sign detection

### 2. Updated Configuration (`backend/app/core/config.py`)
- **Added**: `HF_TOKEN` configuration for Hugging Face API
- **Removed**: `OPENAI_API_KEY` dependency

### 3. Updated Dependencies (`backend/requirements.txt`)
- **Added**: `huggingface_hub==0.19.4`
- **Removed**: `openai==1.3.7`

### 4. Updated Environment Template (`env.example`)
- **Added**: `HF_TOKEN=your_huggingface_token_here`
- **Removed**: `OPENAI_API_KEY` configuration

### 5. Updated Chatbot Service (`backend/app/services/chatbot_service.py`)
- **Modified**: Constructor to use `HuggingFaceService` instead of `OpenAIService`
- **Updated**: Method calls to use the new service

### 6. Updated API Endpoints (`backend/app/api/v1/endpoints/chatbot.py`)
- **Added**: Dependency injection functions for services
- **Updated**: All endpoints to use the new service architecture

## Cybersecurity System Prompt Features

The new system prompt includes:

### Core Expertise Areas:
- Phishing detection and prevention
- Romance scams and catfishing
- Investment and cryptocurrency scams
- Tech support scams
- Identity theft prevention
- Social engineering tactics
- Email security and verification
- Website safety assessment
- Financial fraud patterns

### Response Guidelines:
- **HIGH/CRITICAL threats**: Immediate warnings, emergency contacts, stop communication
- **MEDIUM threats**: Clear explanations, protective measures
- **LOW threats**: General guidance, continued vigilance
- Always provides specific next steps and resources
- Includes relevant contact information for reporting scams

### Key Warning Signs Detected:
- Urgent requests for money or personal information
- Requests for gift cards, wire transfers, or cryptocurrency
- Suspicious email addresses or domains
- Poor grammar and spelling in official communications
- Requests to keep communications secret
- Pressure tactics and artificial urgency
- Unsolicited contact claiming to be from trusted organizations
- Requests for remote access to devices
- Investment opportunities with guaranteed high returns
- Romance scams involving requests for money

## Usage

### Environment Setup
1. Set your Hugging Face token in the environment:
   ```bash
   export HF_TOKEN="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"
   ```

2. Or add it to your `.env` file:
   ```
   HF_TOKEN=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
   ```

### Testing
Run the test script to verify the integration:
```bash
python test_chatbot.py
```

### API Usage
The chatbot API endpoints remain the same:
- `POST /api/v1/chatbot/sessions` - Create new chat session
- `POST /api/v1/chatbot/sessions/{session_id}/messages` - Send message and get AI response
- `GET /api/v1/chatbot/sessions/{session_id}/messages` - Get chat history

## Model Configuration

Currently using `microsoft/DialoGPT-large` for chat completions. This can be easily changed to other models by updating the model parameter in the `HuggingFaceService` class.

## Benefits

1. **Cost Effective**: No OpenAI API costs
2. **Privacy Focused**: Uses open-source models
3. **Specialized**: Cybersecurity-focused system prompt
4. **Comprehensive**: Advanced fraud detection and analysis
5. **Reliable**: Fallback responses when API is unavailable
6. **Educational**: Helps users learn to identify threats

## Security Considerations

- The HF token should be kept secure and not committed to version control
- The system prompt is designed to prioritize user safety
- All responses include warnings for high-risk situations
- Users are always encouraged to verify information through official channels

## Future Enhancements

- Integration with additional threat intelligence feeds
- Real-time model updates
- Custom model fine-tuning for specific fraud types
- Multi-language support
- Voice-based interactions
