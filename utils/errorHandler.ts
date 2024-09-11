import { NextRequest, NextResponse } from 'next/server';

type CallbackFunc = (req: NextRequest) => Promise<NextResponse | Response>;

export default function errorHandler(callbackFunc: CallbackFunc) {
  return async (req: NextRequest) => {
    try {
      return await callbackFunc(req);
    } catch (error) {
      console.error(error);
      return new NextResponse(JSON.stringify({ error: '发生了内部服务器错误' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  };
}