<?php

namespace Tests\Feature;

use App\Http\Illuminate\Validate\PlatValidate;
use App\QSCell\ReportSdkCell;
use Tests\TestCase;
use App\Http\Controllers\Report\ReportController;
use App\Http\Controllers\Config\PlatController;
use App\Http\Controllers\Config\AdController;
use App\Http\Controllers\Info\MediaController;

class ControllerTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function testUnionReportTest()
    {
//        $data = [
//            "begin_date" => 20210621,
//            "end_date" => 20210621,
//            "appid" => "3801556",
//            "appid-opt" => "in",
//            "columns" => [
//                "yyyyMMdd", "sdk_request", "sdk_request_success", "sdk_fill_rate",
//                "sdk_display", "sdk_click","sdk_click_rate","plat_display","plat_click",
//                "plat_click_rate","ecpm","cpc","income","click_gap","display_gap","dau",
//                "average_income"
//            ],
////            "page" => 1,
////            "limit" => 15,
//            'echart' => 1,
////            'excel' => 1
//        ];
//        (new ReportController())->unionReport($data);
    }

    public function testAccountView()
    {
//        $data = [
//            'media_id' =>  12,
//            'sdk_id' => 1
//        ];
//        (new PlatController())->accountView($data);
    }

    public function testPlatAccountAdd()
    {
//        $data = [
//            "media_id" => 12,
//            "sdk_id" => 5,
//            "account" => "默认账号"
//        ];
//
//        (new PlatController)->addAccount($data);
    }

    public function testMediaGet()
    {
//        $data = [
//
//        ];
//
//        (new MediaController())->devGet($data);
    }

//    public function testAppGet()
//    {
//        $data = [
//
//        ];
//
//        (new MediaController())->appGet($data);
//    }
    public function testAdGet()
    {
//        $data = [
//            "page" => 2
//        ];
//
//        (new AdController())->get($data);
    }

    public function testReportSdk()
    {
        $data = [
            "begin_date" => 20210701,
            "end_date" => 20210703,
            "page" => 1,
            "sdk_id" => "all",
            "appid" => 'all',
            "excel" => 1
        ];

        (new ReportController())->sdkReport($data);
    }
}
