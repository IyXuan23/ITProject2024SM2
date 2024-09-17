import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'edge';

export async function POST(req: NextRequest) {
  const body = await req.json();
  const id = body.id;
  const question = body.messages[body.messages.length - 1].text;

  try {
    const url = process.env.BACKEND_URL || 'https://api-test-gamma-nine.vercel.app'
    const response = await fetch(`${url}/api/v0/generate_sql?question=${encodeURIComponent(question)}`, {
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
    return NextResponse.json({ text: data.response, id });
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json({ error: 'failed when processing request' }, { status: 500 });
  }
}

export async function GET(req: NextRequest) {
  try {
    const body = await req.json();
    const { id, question, sql } = body;
    const url = process.env.BACKEND_URL || 'https://api-test-gamma-nine.vercel.app'
    const response = await fetch(`${url}/api/v0/generate_followup_questions`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id, question, sql })
    });

    if (!response.ok) {
      throw new Error('API request failed');
    }

    const data = await response.json();
    // 返回 API 的响应，包括 id
    return NextResponse.json({ data, id });
  } catch (error) {
    console.error('错误:', error);
    return NextResponse.json({ error: 'API request failed' }, { status: 500 });
  }
}