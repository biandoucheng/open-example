<?php
/**
 * Created by PhpStorm.
 * User: 86182
 * Date: 2021/7/2
 * Time: 12:05
 */

namespace Tests\Unit;

use QSM\CellFactory;

class ReportCell extends CellFactory
{
    protected $struct = [
        'yyyyMMdd' => [
            'alias' => '日期',
            'show' => true,
            'where' => 'eq_or_between',
            'group' => true,
            'order' => 'desc'
        ],
        'partner_id' => [
            'alias' => '伙伴ID',
            'show' => true,
            'where' => 'eq_or_in',
            'group' => true,
            'order' => 'asc'
        ],
        'partner_name' => [
            'alias' => '伙伴名称',
            'show_with' => ['partner_id'],
            'attach' => true
        ],
        'member_id' => [
            'alias' => '成员ID',
            'show' => true,
            'group' => true,
            'where' => 'eq_or_in',
            'order' => 'asc'
        ],
        'member' => [
            'alias' => '成员',
            'show_with' => ['member_id'],
            'attach' => true
        ],
        'stat' => [
            'alias' => '状态',
            'show' => true,
            'where' => 'eq_or_in',
            'cal' => 'MIN(`stat`) AS stat'
        ],
        'sale_volume' => [
            'alias' => '销售量',
            'show' => true,
            'cal' => 'IFNULL(SUM(sale_volume),0) AS sale_volume',
            'is_summary_field' => true
        ],
        'back_volume' => [
            'alias' => '退款量',
            'show' => true,
            'cal' => 'IFNULL(SUM(back_volume),0) AS back_volume',
            'is_summary_field' => true
        ],
        'broken_volume' => [
            'alias' => '损坏量',
            'show' => true,
            'cal' => 'IFNULL(SUM(broken_volume),0) AS broken_volume',
            'is_summary_field' => true
        ],
        'earn' => [
            'alias' => '收入',
            'show' => true,
            'cal' => 'IFNULL(ROUND(SUM(earn),2),0.00) AS earn',
            'is_summary_field' => true
        ],
        'earn_ratio' => [
            'alias' => '收入环比',
            'show_with' => ['earn'],
            'cal_attach' => true,
            'is_summary_field' => true
        ]
    ];

    public function __construct()
    {
        parent::__construct();
        $this->outPut->limit = 30;
        $this->outPut->excelName = "销售报表.csv";
        $this->outPut->summary = true;
    }
}