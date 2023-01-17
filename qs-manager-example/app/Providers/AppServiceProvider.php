<?php

namespace App\Providers;

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{

    protected $customerMsg = [

    ];
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        #sql打印
        DB::listen(function ($query) {
            $sq = $query->sql .PHP_EOL. json_encode($query->bindings).PHP_EOL.$query->time.PHP_EOL;
            Log::channel('sql')->debug($sq);
        });
    }
}
