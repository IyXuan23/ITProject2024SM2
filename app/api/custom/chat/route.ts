import { DeepChatTextRequestBody } from '../../../../types/deepChatTextRequestBody';
import errorHandler from '../../../../utils/errorHandler';
import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'edge';

async function handler(req: NextRequest) {
  const messageRequestBody = (await req.json()) as DeepChatTextRequestBody;
  console.log(messageRequestBody);
  return NextResponse.json({ text: 'This is a response from a NextJS edge server. Thank you for your message!' });
}

export async function POST(req: NextRequest) {
  const body = await req.json();
  const question = body.messages[body.messages.length - 1].text;

  try {
    const apiUrl = process.env.API_URL || 'http://localhost:5328';
    const response = await fetch(`${apiUrl}/api/v0/generate_sql?question=${encodeURIComponent(question)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('API request failed');
    }

    const data = await response.json();

    // Return the response from the API
    return NextResponse.json({ text: data.response });
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json({ error: 'failed when processing request' }, { status: 500 });
  }
}

export async function GET(req: NextRequest) {
  try {
    const apiUrl = process.env.API_URL || 'http://localhost:5328';
    const response = await fetch(`${apiUrl}/api/v0/generate_questions`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('API request failed');
    }

    const data = await response.json();

    return NextResponse.json(data);
  } catch (error) {
    console.error('Error generating questions:', error);
    return NextResponse.json({ error: 'Retrieve suggest questions failed' }, { status: 500 });
  }
}