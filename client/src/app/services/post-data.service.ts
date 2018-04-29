import { Injectable } from '@angular/core';
import {Observable} from "rxjs/Observable";
import {HttpClient} from "@angular/common/http";

@Injectable()
export class PostDataService {

  private BaseUrl = 'http://localhost:8080';
  constructor(private  http: HttpClient) { }
  postData(data: any): Observable<any> {
    let tipData = data.constructor.name;
    let url = `${this.BaseUrl}/${tipData}`;
    console.log(url);
    return this.http.post(url, data);
  }

}
