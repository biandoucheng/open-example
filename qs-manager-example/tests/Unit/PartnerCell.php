<?php
/**
 * Created by PhpStorm.
 * User: 86182
 * Date: 2021/7/2
 * Time: 11:46
 */

namespace Tests\Unit;

use QSM\CellFactory;

class PartnerCell extends CellFactory
{
    protected $struct = [
        'partner_id' => [
            'alias' => '伙伴ID',
            'show' => true,
            'field' => 'id',
            'where' => 'eq_or_in'
        ],
        'part_type' => [
            'alias' => '伙伴类型',
            'show' => true,
            'where' => '='
        ],
        'username' => [
            'alias' => '用户名',
            'show' => true,
            'where' => 'like'
        ],
        'company' => [
            'alias' => '公司名称',
            'show' => true,
            'where' => 'like'
        ],
        'member_num' => [
            'alias' => '成员数量',
            'show' => true
        ],
        'invite_id' => [
            'alias' => '邀请人ID',
            'show' => true,
            'where' => 'eq_or_in'
        ],
        'invite_man' => [
            'alias' => '邀请人',
            'where' => 'like',
            'attach' => true,
            'show_with' => ['invite_id']
        ],
        'status' => [
            'alias' => '伙伴状态',
            'show' => true,
            'where' => '='
        ],
        'lastmod_time' => [
            'alias' => '修改时间',
            'show' => true,
            'order' => 'desc'
        ],
        'accept_time' => [
            'alias' => '创建时间',
            'show' => true,
            'order' => 'desc'
        ]
    ];

    public function __construct()
    {
        parent::__construct();
        $this->outPut->limit = 30;
        $this->outPut->excelName = "伙伴信息列表.csv";
        $this->outPut->attachFields = ['id','invite_id'];
    }
}