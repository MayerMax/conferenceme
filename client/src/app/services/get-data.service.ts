import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs/Observable";

@Injectable()
export class GetDataService {
  private BaseUrl = 'http://localhost:8080';
  constructor(private  http: HttpClient) { }
  getData(tipData: string): Observable<any> {
    let url = `${this.BaseUrl}${tipData}`;
    return this.http.get(url);
  }

}
