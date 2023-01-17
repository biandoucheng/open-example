<?php
/**
 * Created by PhpStorm.
 * User: 86182
 * Date: 2021/6/15
 * Time: 17:32
 */
namespace Tests\Unit;

use Illuminate\Support\Facades\DB;
use Tests\CreatesApplication;
use QSM\QSManager;
use QSM\QSModel;
use Illuminate\Database\Eloquent\Model;
use App\Model\Partner;
use App\Model\Team;
use App\Model\SaleReport;
use Tests\TestCase;
use QSM\CellFactory;
use Tests\Unit\PartnerCell;
use Tests\Unit\ReportCell;

class QSManagerTest extends TestCase
{
    #合作伙伴，查询
    protected $partner = [
        'partner_id' => [2,3,4,5,6,7,8,9],
//        'part_type' => 1
    ];

    #合作伙伴报表查询
    protected $report = [
        'yyyyMMdd' => [20210601],
        'partner_id' => 12,
        'status' => 0
    ];

    /**
     *@description 测试QSManager
     *
     *@author biandou
     *@date 2021/6/18 17:32
     */
    public function testQsManager()
    {
        $qsm = new QSManager();

        #合作伙伴
        $qs = $qsm->load(
            new PartnerCell(),
            $this->partner
        );

        #查询
        $model = new QSModel();
        $model->search("",new Partner(),$qs);
        print_r($model->result);

//        #合作伙伴销售报表
//        $qs = $qsm->load(
//            new ReportCell(),
//            $this->report,
//            [
//                "partner_id" => [
//                    "opt" => "neq_or_nin",
//                    "order" => "DESC",
//                    "index" => 1,
//                    "alias" => "兄弟"
//                ]
//            ]
//        );
//
//        #查询
//        $model = new QSModel();
//        $model->search("",new SaleReport(),$qs);
//        print_r($model->result->toResponse());
    }
}