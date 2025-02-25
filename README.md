# LINE Bot with Vertex AI Agent Builder

## Project Introduction
This project demonstrates how to use LINE Bot and Vertex AI Agent Builder to create a travel information inquiry robot. Users can enter travel-related questions in LINE, and the robot will search Google Search and enterprise data through Vertex AI Agent Builder and answer users' questions in natural language.

## Features
* Users can enter travel-related questions in LINE.
* The robot will search Google Search and enterprise data through Vertex AI Agent Builder.
* The robot will answer users' questions in natural language.

## Technology
* LINE Messaging API
* Vertex AI Agent Builder
* Google Cloud Run
* Python

## Architecture


## Deployment
1. Create a LINE Bot account.
2. Create a Cloud Run service on GCP.
3. Set the Channel Secret and Channel Access Token of LINE Bot to the environment variables of the Cloud Run service.
4. Deploy the code to the Cloud Run service.
5. Set the Webhook URL in the LINE Bot settings.

## Usage
1. Add the robot as a friend in LINE.
2. Enter travel-related questions in LINE.
3. The robot will answer your questions in natural language.

## References
* LINE Messaging API documentation: https://developers.line.biz/en/docs/messaging-api/
* Vertex AI Agent Builder documentation: https://cloud.google.com/vertex-ai/docs/agent-builder/overview
* Google Cloud Run documentation: https://cloud.google.com/run/docs/
* Python documentation: https://www.python.org/doc/

## Precautions
* This project is for demonstration purposes only and does not guarantee its availability or security.
* This project uses some GCP services, which may incur some costs.
* The code of this project is for reference only, please modify it according to your actual needs.

## Disclaimer
The author of this project is not responsible for any loss or damage caused by the use of this project.

## Contact
If you have any questions, please contact [your email address].

## License
The code of this project uses the MIT license.
